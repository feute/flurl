drop table if exists urls;
create table urls (
	id integer primary key autoincrement,
	short text unique not null,
	original text not null
);
