CREATE TABLE IF NOT EXISTS humans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    birthplace VARCHAR(255) NOT NULL,
    gender VARCHAR(255) NOT NULL,
    culture VARCHAR(255) NOT NULL,
    status VARCHAR(255) DEFAULT 'missing', 
    biography TEXT,
    comments TEXT,
    discovery TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (name, birthplace, birthday)
);

CREATE TABLE IF NOT EXISTS families (
    id SERIAL PRIMARY KEY,
    related_human_id INTEGER REFERENCES humans(id) ON DELETE CASCADE NOT NULL,
    relation_type VARCHAR(50) NOT NULL, 
    human_name VARCHAR(255) NOT NULL,
    human_id INTEGER,
    comments TEXT,
    UNIQUE (related_human_id, relation_type, human_name)
);

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    related_human_id INTEGER REFERENCES humans(id) ON DELETE CASCADE,
    identifier_type VARCHAR(50) NOT NULL,
    source TEXT NOT NULL, 
    comments TEXT,
    discovery TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(related_human_id, identifier_type, source)
);

