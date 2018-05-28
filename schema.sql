drop table if exists entries;
create table entries (
  id integer primary key AUTO_INCREMENT,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  content TEXT NOT NULL,
  date DATE not null ,
  author TEXT NOT NULL,
  tags TEXT NOT NULL
);