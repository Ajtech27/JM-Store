from market import create_app, db
from market.model import User, Item

app = create_app()

def seed_items():
    """Add default items to the database if they don't exist."""
    
    if Item.query.count() == 0:
        default_items = [
            Item(
                name="Laptop",
                price=1200,
                barcode="LAP12345",
                description="High-performance laptop with 16GB RAM"
            ),
            Item(
                name="Mouse",
                price=25,
                barcode="MSE67890",
                description="Wireless ergonomic mouse"
            ),
            Item(
                name="Keyboard",
                price=50,
                barcode="KEY54321",
                description="Mechanical gaming keyboard"
            ),
            Item(
                name="Monitor",
                price=300,
                barcode="MON98765",
                description="27-inch 4K monitor"
            ) ]
 
        db.session.add_all(default_items)
        db.session.commit()
        print("✅ Default items added to the database!")
    else:
        print("ℹ️ Items already exist. Skipping seeding.")

# Create tables and seed items
with app.app_context():
    db.create_all()
    seed_items()
    print("✅ Database ready!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 