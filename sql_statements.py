DROP_GINS = '''
    DROP TABLE IF EXISTS gins;
'''
DROP_GARNISHES = '''
    DROP TABLE IF EXISTS garnishes;
'''
DROP_TONICS = '''
    DROP TABLE IF EXISTS tonics;
'''
DROP_PERFECT_GARNISHES = '''
    DROP TABLE IF EXISTS perfect_garnishes;
'''
DROP_PERFECT_TONICS = '''
    DROP TABLE IF EXISTS perfect_tonics;
'''

CREATE_GINS = '''
    CREATE TABLE gins(
        id integer NOT NULL, 
        type varchar NOT NULL, 
        name varchar,
        first_name varchar, 
        second_name varchar, 
        picture_url varchar,
        producer varchar, 
        country varchar, 
        abv integer, 
        average_rating integer, 
        rating_count integer,
        content varchar, 
        google_translation varchar,
        original_content varchar
    );
'''

CREATE_GARNISHES = '''
    CREATE TABLE garnishes(
        id integer NOT NULL, 
        type varchar NOT NULL, 
        name varchar,
        first_name varchar, 
        second_name varchar, 
        picture_url varchar,
        producer varchar, 
        country varchar, 
        abv integer, 
        average_rating integer, 
        rating_count integer,
        content varchar, 
        google_translation varchar,
        original_content varchar
    );
'''
CREATE_TONICS = '''
    CREATE TABLE tonics(
        id integer NOT NULL, 
        type character varying NOT NULL, 
        name character varying,
        first_name character varying, 
        second_name character varying, 
        picture_url character varying,
        producer character varying, 
        country character varying, 
        abv integer, 
        average_rating integer, 
        rating_count integer,
        content character varying, 
        google_translation character varying,
        original_content character varying
    );
'''
CREATE_PERFECT_GARNISHES = '''
    CREATE TABLE perfect_garnishes(
        id integer NOT NULL,
        perfect_garnish integer NOT NULL
    );
'''
CREATE_PERFECT_TONICS = '''
    CREATE TABLE perfect_tonics(
        id integer NOT NULL,
        perfect_tonic integer NOT NULL
    );
'''

drop_statements = [
    DROP_GINS,
    DROP_TONICS,
    DROP_GARNISHES,
    DROP_PERFECT_GARNISHES,
    DROP_PERFECT_TONICS,
    ]

create_statements = [
    CREATE_GINS,
    CREATE_TONICS,
    CREATE_GARNISHES,
    CREATE_PERFECT_GARNISHES,
    CREATE_PERFECT_TONICS,
    ]
