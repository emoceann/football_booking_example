create extension postgis;

create table users
(
    id       bigserial primary key,
    username varchar(256) unique,
    password varchar(2048),
    type     varchar(32)
);

create table football_fields
(
    id           bigserial primary key,
    owner_id     bigserial,
    booking_rate integer,
    name         varchar(256) unique,
    contact      varchar(36),
    geom         geometry(Point, 4326),
    images       jsonb,
    constraint fk_owner
        foreign key (owner_id)
            references users (id)
);

create table bookings
(
    id          bigserial primary key,
    user_book   bigserial,
    field_name  varchar(256),
    start_date  timestamp without time zone,
    finish_date timestamp without time zone,
    constraint fk_user_book
        foreign key (user_book)
            references users (id),
    constraint fk_field_name
        foreign key (field_name)
            references football_fields (name)
);

create index football_fields_geom_idx
    on football_fields
        using GIST (geom);