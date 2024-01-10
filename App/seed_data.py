from restaurant import Base, engine, session, Customer, Restaurant, Review


customer1 = Customer(first_name='Thunder', last_name='cat')
customer2 = Customer(first_name='Jeremy', last_name='Doku')

restaurant1 = Restaurant(name='Durag', price=5)
restaurant2 = Restaurant(name='Citeh', price=2)

review1 = Review(customer=customer1, restaurant=restaurant1, star_rating=4)
review2 = Review(customer=customer2, restaurant=restaurant1, star_rating=5)


session.add_all([customer1, customer2, restaurant1, restaurant2, review1, review2])
session.commit()


print(customer1.full_name()) 
print(customer2.favorite_restaurant().name)  


customer1.add_review(restaurant2, 3)
customer1.delete_reviews(restaurant1)


print(review1.full_review())  
print(Restaurant.fanciest().name)  
print('\n'.join(restaurant1.all_reviews()))