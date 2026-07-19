from datetime import datetime
import hashlib
from src.models.user import db


class UserLocation(db.Model):
    """
    Model for tracking unique user locations persistently.
    This data persists even after chat logs are cleaned up.
    Locations are stored at city level for privacy.
    """
    __tablename__ = 'user_locations'

    id = db.Column(db.Integer, primary_key=True)

    # Hash of IP address (for deduplication without storing actual IP)
    ip_hash = db.Column(db.String(64), unique=True, nullable=False)

    # Location data (city-level for privacy)
    country = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)

    # Coordinates rounded to ~1km precision for privacy
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Metadata
    first_seen = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    visit_count = db.Column(db.Integer, default=1, nullable=False)

    @staticmethod
    def hash_ip(ip_address):
        """Create a hash of the IP address for privacy-preserving deduplication"""
        if not ip_address:
            return None
        return hashlib.sha256(ip_address.encode()).hexdigest()

    @staticmethod
    def round_coordinate(coord, precision=2):
        """Round coordinate for privacy (~1km at precision=2)"""
        if coord is None:
            return None
        return round(coord, precision)

    @classmethod
    def record_location(cls, ip_address, location_data):
        """
        Record a user location. Updates existing record or creates new one.
        Returns the location record.
        """
        if not ip_address or not location_data:
            return None

        ip_hash = cls.hash_ip(ip_address)
        if not ip_hash:
            return None

        # Round coordinates for privacy
        lat = cls.round_coordinate(location_data.get('latitude'))
        lng = cls.round_coordinate(location_data.get('longitude'))

        # Skip if no valid coordinates
        if lat is None or lng is None:
            return None

        try:
            # Check if this IP has been seen before
            existing = cls.query.filter_by(ip_hash=ip_hash).first()

            if existing:
                # Update last seen and visit count
                existing.last_seen = datetime.utcnow()
                existing.visit_count += 1
                db.session.commit()
                return existing
            else:
                # Create new location record
                new_location = cls(
                    ip_hash=ip_hash,
                    country=location_data.get('country'),
                    region=location_data.get('region'),
                    city=location_data.get('city'),
                    latitude=lat,
                    longitude=lng
                )
                db.session.add(new_location)
                db.session.commit()
                return new_location
        except Exception as e:
            print(f"[ERROR] Failed to record location: {e}")
            db.session.rollback()
            return None

    @classmethod
    def import_records(cls, records):
        """
        Import location records previously exported via to_dict().
        Exported records don't include ip_hash (it's private), so imported rows
        get a synthetic hash derived from the location itself for deduplication.
        Returns (imported_count, skipped_count).
        """
        imported = 0
        skipped = 0
        for rec in records:
            try:
                lat = rec.get('latitude')
                lng = rec.get('longitude')
                if lat is None or lng is None:
                    skipped += 1
                    continue

                synthetic_key = f"import:{rec.get('country')}:{rec.get('city')}:{lat}:{lng}"
                ip_hash = hashlib.sha256(synthetic_key.encode()).hexdigest()

                if cls.query.filter_by(ip_hash=ip_hash).first():
                    skipped += 1
                    continue

                # Also skip if an organically-recorded row already sits at the
                # same rounded coordinates + city (avoids visual duplicates).
                if cls.query.filter_by(latitude=lat, longitude=lng, city=rec.get('city')).first():
                    skipped += 1
                    continue

                row = cls(
                    ip_hash=ip_hash,
                    country=rec.get('country'),
                    region=rec.get('region'),
                    city=rec.get('city'),
                    latitude=lat,
                    longitude=lng,
                    visit_count=rec.get('visit_count') or 1
                )
                if rec.get('first_seen'):
                    row.first_seen = datetime.fromisoformat(rec['first_seen'])
                if rec.get('last_seen'):
                    row.last_seen = datetime.fromisoformat(rec['last_seen'])
                db.session.add(row)
                imported += 1
            except Exception:
                db.session.rollback()
                skipped += 1
        db.session.commit()
        return imported, skipped

    @classmethod
    def get_all_locations(cls):
        """Get all unique locations for the map"""
        return cls.query.all()

    @classmethod
    def get_location_stats(cls):
        """Get statistics about locations"""
        from sqlalchemy import func

        total_locations = cls.query.count()
        total_visits = db.session.query(func.sum(cls.visit_count)).scalar() or 0

        countries = db.session.query(
            cls.country,
            func.count(cls.id).label('count')
        ).filter(cls.country.isnot(None)).group_by(cls.country).all()

        return {
            'total_unique_locations': total_locations,
            'total_visits': total_visits,
            'by_country': {c: count for c, count in countries}
        }

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'country': self.country,
            'region': self.region,
            'city': self.city,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'visit_count': self.visit_count
        }
