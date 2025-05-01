from typing import Any, List, Optional

from sqlalchemy import CHAR, Column, DECIMAL, DateTime, Enum, ForeignKeyConstraint, Index, Integer, LargeBinary, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import MEDIUMINT, SET, SMALLINT, TINYINT, VARCHAR, YEAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import NullType
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Actor(Base):
    __tablename__ = 'actor'
    __table_args__ = (
        Index('idx_actor_last_name', 'last_name'),
    )

    actor_id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(45))
    last_name: Mapped[str] = mapped_column(String(45))
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    film_actor: Mapped[List['FilmActor']] = relationship('FilmActor', back_populates='actor')


t_actor_info = Table(
    'actor_info', Base.metadata,
    Column('actor_id', SMALLINT, server_default=text("'0'")),
    Column('first_name', String(45)),
    Column('last_name', String(45)),
    Column('film_info', Text)
)


class Category(Base):
    __tablename__ = 'category'

    category_id: Mapped[int] = mapped_column(TINYINT, primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    film_category: Mapped[List['FilmCategory']] = relationship('FilmCategory', back_populates='category')


class Country(Base):
    __tablename__ = 'country'

    country_id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    country: Mapped[str] = mapped_column(String(50))
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    city: Mapped[List['City']] = relationship('City', back_populates='country')


t_customer_list = Table(
    'customer_list', Base.metadata,
    Column('ID', SMALLINT, server_default=text("'0'")),
    Column('name', String(91)),
    Column('address', String(50)),
    Column('zip code', String(10)),
    Column('phone', String(20)),
    Column('city', String(50)),
    Column('country', String(50)),
    Column('notes', String(6)),
    Column('SID', TINYINT)
)


t_film_list = Table(
    'film_list', Base.metadata,
    Column('FID', SMALLINT, server_default=text("'0'")),
    Column('title', String(128)),
    Column('description', Text),
    Column('category', String(25)),
    Column('price', DECIMAL(4, 2), server_default=text("'4.99'")),
    Column('length', SMALLINT),
    Column('rating', Enum('G', 'PG', 'PG-13', 'R', 'NC-17'), server_default=text("'G'")),
    Column('actors', Text)
)


class FilmText(Base):
    __tablename__ = 'film_text'
    __table_args__ = (
        Index('idx_title_description', 'title', 'description'),
    )

    film_id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)


class Language(Base):
    __tablename__ = 'language'

    language_id: Mapped[int] = mapped_column(TINYINT, primary_key=True)
    name: Mapped[str] = mapped_column(CHAR(20))
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    film: Mapped[List['Film']] = relationship('Film', foreign_keys='[Film.language_id]', back_populates='language')
    film_: Mapped[List['Film']] = relationship('Film', foreign_keys='[Film.original_language_id]', back_populates='original_language')


t_nicer_but_slower_film_list = Table(
    'nicer_but_slower_film_list', Base.metadata,
    Column('FID', SMALLINT, server_default=text("'0'")),
    Column('title', String(128)),
    Column('description', Text),
    Column('category', String(25)),
    Column('price', DECIMAL(4, 2), server_default=text("'4.99'")),
    Column('length', SMALLINT),
    Column('rating', Enum('G', 'PG', 'PG-13', 'R', 'NC-17'), server_default=text("'G'")),
    Column('actors', Text)
)


t_sales_by_film_category = Table(
    'sales_by_film_category', Base.metadata,
    Column('category', String(25)),
    Column('total_sales', DECIMAL(27, 2))
)


t_sales_by_store = Table(
    'sales_by_store', Base.metadata,
    Column('store', String(101)),
    Column('manager', String(91)),
    Column('total_sales', DECIMAL(27, 2))
)


class Staff(Base):
    __tablename__ = 'staff'
    __table_args__ = (
        ForeignKeyConstraint(['address_id'], ['address.address_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_staff_address'),
        ForeignKeyConstraint(['store_id'], ['store.store_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_staff_store'),
        Index('idx_fk_address_id', 'address_id'),
        Index('idx_fk_store_id', 'store_id')
    )

    staff_id: Mapped[int] = mapped_column(TINYINT, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(45))
    last_name: Mapped[str] = mapped_column(String(45))
    address_id: Mapped[int] = mapped_column(SMALLINT)
    store_id: Mapped[int] = mapped_column(TINYINT)
    active: Mapped[int] = mapped_column(TINYINT(1), server_default=text("'1'"))
    username: Mapped[str] = mapped_column(String(16))
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    picture: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    email: Mapped[Optional[str]] = mapped_column(String(50))
    password: Mapped[Optional[str]] = mapped_column(VARCHAR(40))

    address: Mapped['Address'] = relationship('Address', back_populates='staff')
    store: Mapped['Store'] = relationship('Store', foreign_keys=[store_id], back_populates='staff')
    store_: Mapped[List['Store']] = relationship('Store', foreign_keys='[Store.manager_staff_id]', back_populates='manager_staff')
    rental: Mapped[List['Rental']] = relationship('Rental', back_populates='staff')
    payment: Mapped[List['Payment']] = relationship('Payment', back_populates='staff')


t_staff_list = Table(
    'staff_list', Base.metadata,
    Column('ID', TINYINT, server_default=text("'0'")),
    Column('name', String(91)),
    Column('address', String(50)),
    Column('zip code', String(10)),
    Column('phone', String(20)),
    Column('city', String(50)),
    Column('country', String(50)),
    Column('SID', TINYINT)
)


class Store(Base):
    __tablename__ = 'store'
    __table_args__ = (
        ForeignKeyConstraint(['address_id'], ['address.address_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_store_address'),
        ForeignKeyConstraint(['manager_staff_id'], ['staff.staff_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_store_staff'),
        Index('idx_fk_address_id', 'address_id'),
        Index('idx_unique_manager', 'manager_staff_id', unique=True)
    )

    store_id: Mapped[int] = mapped_column(TINYINT, primary_key=True)
    manager_staff_id: Mapped[int] = mapped_column(TINYINT)
    address_id: Mapped[int] = mapped_column(SMALLINT)
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    staff: Mapped[List['Staff']] = relationship('Staff', foreign_keys='[Staff.store_id]', back_populates='store')
    address: Mapped['Address'] = relationship('Address', back_populates='store')
    manager_staff: Mapped['Staff'] = relationship('Staff', foreign_keys=[manager_staff_id], back_populates='store_')
    inventory: Mapped[List['Inventory']] = relationship('Inventory', back_populates='store')
    customer: Mapped[List['Customer']] = relationship('Customer', back_populates='store')


class City(Base):
    __tablename__ = 'city'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['country.country_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_city_country'),
        Index('idx_fk_country_id', 'country_id')
    )

    city_id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    city: Mapped[str] = mapped_column(String(50))
    country_id: Mapped[int] = mapped_column(SMALLINT)
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    country: Mapped['Country'] = relationship('Country', back_populates='city')
    address: Mapped[List['Address']] = relationship('Address', back_populates='city')


class Film(Base):
    __tablename__ = 'film'
    __table_args__ = (
        ForeignKeyConstraint(['language_id'], ['language.language_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_film_language'),
        ForeignKeyConstraint(['original_language_id'], ['language.language_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_film_language_original'),
        Index('idx_fk_language_id', 'language_id'),
        Index('idx_fk_original_language_id', 'original_language_id'),
        Index('idx_title', 'title')
    )

    film_id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    language_id: Mapped[int] = mapped_column(TINYINT)
    rental_duration: Mapped[int] = mapped_column(TINYINT, server_default=text("'3'"))
    rental_rate: Mapped[decimal.Decimal] = mapped_column(DECIMAL(4, 2), server_default=text("'4.99'"))
    replacement_cost: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), server_default=text("'19.99'"))
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    release_year: Mapped[Optional[Any]] = mapped_column(YEAR)
    original_language_id: Mapped[Optional[int]] = mapped_column(TINYINT)
    length: Mapped[Optional[int]] = mapped_column(SMALLINT)
    rating: Mapped[Optional[str]] = mapped_column(Enum('G', 'PG', 'PG-13', 'R', 'NC-17'), server_default=text("'G'"))
    special_features: Mapped[Optional[str]] = mapped_column(SET('Trailers', 'Commentaries', 'Deleted Scenes', 'Behind the Scenes'))

    language: Mapped['Language'] = relationship('Language', foreign_keys=[language_id], back_populates='film')
    original_language: Mapped[Optional['Language']] = relationship('Language', foreign_keys=[original_language_id], back_populates='film_')
    film_actor: Mapped[List['FilmActor']] = relationship('FilmActor', back_populates='film')
    film_category: Mapped[List['FilmCategory']] = relationship('FilmCategory', back_populates='film')
    inventory: Mapped[List['Inventory']] = relationship('Inventory', back_populates='film')


class Address(Base):
    __tablename__ = 'address'
    __table_args__ = (
        ForeignKeyConstraint(['city_id'], ['city.city_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_address_city'),
        Index('idx_fk_city_id', 'city_id'),
        Index('idx_location', 'location')
    )

    address_id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    address: Mapped[str] = mapped_column(String(50))
    district: Mapped[str] = mapped_column(String(20))
    city_id: Mapped[int] = mapped_column(SMALLINT)
    phone: Mapped[str] = mapped_column(String(20))
    location: Mapped[str] = mapped_column(NullType)
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    address2: Mapped[Optional[str]] = mapped_column(String(50))
    postal_code: Mapped[Optional[str]] = mapped_column(String(10))

    staff: Mapped[List['Staff']] = relationship('Staff', back_populates='address')
    store: Mapped[List['Store']] = relationship('Store', back_populates='address')
    city: Mapped['City'] = relationship('City', back_populates='address')
    customer: Mapped[List['Customer']] = relationship('Customer', back_populates='address')


class FilmActor(Base):
    __tablename__ = 'film_actor'
    __table_args__ = (
        ForeignKeyConstraint(['actor_id'], ['actor.actor_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_film_actor_actor'),
        ForeignKeyConstraint(['film_id'], ['film.film_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_film_actor_film'),
        Index('idx_fk_film_id', 'film_id')
    )

    actor_id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    film_id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    actor: Mapped['Actor'] = relationship('Actor', back_populates='film_actor')
    film: Mapped['Film'] = relationship('Film', back_populates='film_actor')


class FilmCategory(Base):
    __tablename__ = 'film_category'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['category.category_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_film_category_category'),
        ForeignKeyConstraint(['film_id'], ['film.film_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_film_category_film'),
        Index('fk_film_category_category', 'category_id')
    )

    film_id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    category_id: Mapped[int] = mapped_column(TINYINT, primary_key=True)
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    category: Mapped['Category'] = relationship('Category', back_populates='film_category')
    film: Mapped['Film'] = relationship('Film', back_populates='film_category')


class Inventory(Base):
    __tablename__ = 'inventory'
    __table_args__ = (
        ForeignKeyConstraint(['film_id'], ['film.film_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_inventory_film'),
        ForeignKeyConstraint(['store_id'], ['store.store_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_inventory_store'),
        Index('idx_fk_film_id', 'film_id'),
        Index('idx_store_id_film_id', 'store_id', 'film_id')
    )

    inventory_id: Mapped[int] = mapped_column(MEDIUMINT, primary_key=True)
    film_id: Mapped[int] = mapped_column(SMALLINT)
    store_id: Mapped[int] = mapped_column(TINYINT)
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    film: Mapped['Film'] = relationship('Film', back_populates='inventory')
    store: Mapped['Store'] = relationship('Store', back_populates='inventory')
    rental: Mapped[List['Rental']] = relationship('Rental', back_populates='inventory')


class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = (
        ForeignKeyConstraint(['address_id'], ['address.address_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_customer_address'),
        ForeignKeyConstraint(['store_id'], ['store.store_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_customer_store'),
        Index('idx_fk_address_id', 'address_id'),
        Index('idx_fk_store_id', 'store_id'),
        Index('idx_last_name', 'last_name')
    )

    customer_id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    store_id: Mapped[int] = mapped_column(TINYINT)
    first_name: Mapped[str] = mapped_column(String(45))
    last_name: Mapped[str] = mapped_column(String(45))
    address_id: Mapped[int] = mapped_column(SMALLINT)
    active: Mapped[int] = mapped_column(TINYINT(1), server_default=text("'1'"))
    create_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    email: Mapped[Optional[str]] = mapped_column(String(50))
    last_update: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    address: Mapped['Address'] = relationship('Address', back_populates='customer')
    store: Mapped['Store'] = relationship('Store', back_populates='customer')
    rental: Mapped[List['Rental']] = relationship('Rental', back_populates='customer')
    payment: Mapped[List['Payment']] = relationship('Payment', back_populates='customer')


class Rental(Base):
    __tablename__ = 'rental'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_rental_customer'),
        ForeignKeyConstraint(['inventory_id'], ['inventory.inventory_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_rental_inventory'),
        ForeignKeyConstraint(['staff_id'], ['staff.staff_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_rental_staff'),
        Index('idx_fk_customer_id', 'customer_id'),
        Index('idx_fk_inventory_id', 'inventory_id'),
        Index('idx_fk_staff_id', 'staff_id'),
        Index('rental_date', 'rental_date', 'inventory_id', 'customer_id', unique=True)
    )

    rental_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rental_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    inventory_id: Mapped[int] = mapped_column(MEDIUMINT)
    customer_id: Mapped[int] = mapped_column(SMALLINT)
    staff_id: Mapped[int] = mapped_column(TINYINT)
    last_update: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    return_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    customer: Mapped['Customer'] = relationship('Customer', back_populates='rental')
    inventory: Mapped['Inventory'] = relationship('Inventory', back_populates='rental')
    staff: Mapped['Staff'] = relationship('Staff', back_populates='rental')
    payment: Mapped[List['Payment']] = relationship('Payment', back_populates='rental')


class Payment(Base):
    __tablename__ = 'payment'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_payment_customer'),
        ForeignKeyConstraint(['rental_id'], ['rental.rental_id'], ondelete='SET NULL', onupdate='CASCADE', name='fk_payment_rental'),
        ForeignKeyConstraint(['staff_id'], ['staff.staff_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_payment_staff'),
        Index('fk_payment_rental', 'rental_id'),
        Index('idx_fk_customer_id', 'customer_id'),
        Index('idx_fk_staff_id', 'staff_id')
    )

    payment_id: Mapped[int] = mapped_column(SMALLINT, primary_key=True)
    customer_id: Mapped[int] = mapped_column(SMALLINT)
    staff_id: Mapped[int] = mapped_column(TINYINT)
    amount: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2))
    payment_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    rental_id: Mapped[Optional[int]] = mapped_column(Integer)
    last_update: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    customer: Mapped['Customer'] = relationship('Customer', back_populates='payment')
    rental: Mapped[Optional['Rental']] = relationship('Rental', back_populates='payment')
    staff: Mapped['Staff'] = relationship('Staff', back_populates='payment')
