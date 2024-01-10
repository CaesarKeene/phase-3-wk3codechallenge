# Import necessary modules and functions from SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import desc


Base = declarative_base()


engine = create_engine('sqlite:///restaurant_database.db')


session = Session(engine)

# Define a Customer class representing the 'customers' table
class Customer(Base):
    __tablename__ = 'customers'  

    
    id = Column(Integer, primary_key=True)  
    first_name = Column(String) 
    last_name = Column(String)  

    # Establish a relationship with the Review class
    reviews = relationship('Review', back_populates='customer')  

    # Method to get the full name of the customer
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Method to find the favorite restaurant of the customer based on highest rated review
    def favorite_restaurant(self):
        highest_rated_review = max(self.reviews, key=lambda review: review.star_rating, default=None)
        return highest_rated_review.restaurant if highest_rated_review else None

    # Method to add a review for a restaurant by the customer
    def add_review(self, restaurant, rating):
        new_review = Review(customer=self, restaurant=restaurant, star_rating=rating)
        session.add(new_review)
        session.commit()

   
    def delete_reviews(self, restaurant):
        for review in self.reviews:
            if review.restaurant == restaurant:
                session.delete(review)
        session.commit()

# Define a Restaurant class representing the 'restaurants' table
class Restaurant(Base):
    __tablename__ = 'restaurants'  

    
    id = Column(Integer, primary_key=True)  
    name = Column(String)  
    price = Column(Integer)  

    
    reviews = relationship('Review', back_populates='restaurant')  

    
    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(desc(cls.price)).first()

    def all_reviews(self):
        review_strings = [
            f"Review for {self.name} by {review.customer.full_name()}: {review.star_rating} stars."
            for review in self.reviews
        ]
        return review_strings

# Define a Review class representing the 'reviews' table
class Review(Base):
    __tablename__ = 'reviews'  

    id = Column(Integer, primary_key=True) 
    star_rating = Column(Integer)  
    customer_id = Column(Integer, ForeignKey('customers.id'))  
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))  

    
    customer = relationship('Customer', back_populates='reviews')  
    restaurant = relationship('Restaurant', back_populates='reviews') 

    
    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

