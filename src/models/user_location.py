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
