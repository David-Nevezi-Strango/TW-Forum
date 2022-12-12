create table Tags (
    tag_id int auto_increment primary key,
    tag_name varchar(50) not null
);

create table Users (
    user_id int auto_increment primary key,
    username varchar(50) not null,
    password varchar(50) not null,
    mail varchar(50) not null,
    name varchar(50),
    unique(username),
    unique (mail)
);

create table Discussions(
    discussion_id int auto_increment primary key,
    tag_id int not null,
    title varchar(50) not null,
    foreign key (tag_id) references Tags(tag_id)
);


create table Comments (
    comment_id int auto_increment primary key,
    user_id int not null,
    discussion_id int not null,
    date date not null,
    text varchar(500) not null,
    -- primary key (comment_id, user_id, discussion_id, date),
    foreign key (discussion_id) references Discussions(discussion_id),
    foreign key (user_id) references Users(user_id)
);

create table Preferences (
    preference_id int auto_increment primary key,
    user_id int not null,
    tag_id int not null,
    -- primary key(preference_id, user_id, tag_id),
    foreign key (user_id) references Users(user_id),
    foreign key (tag_id) references Tags(tag_id)
);


drop table Comments;
drop table Preferences;
drop table Discussions;
drop table Tags;
drop table Users;