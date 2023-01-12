create table Tags (
    tag_id int auto_increment primary key,
    tag_name varchar(50) not null
);

create table Notifications (
	notification_id int auto_increment primary key,
    text varchar(250) not null,
    date date not null
);

create table Users (
    user_id int auto_increment primary key,
    username varchar(50) not null,
    password varchar(256) not null,
    mail varchar(50) not null,
    name varchar(50),
    last_notification_id int not null,
    foreign key (last_notification_id) references Notifications(notification_id),
    unique(username),
    unique (mail)
);

create table Discussions(
    discussion_id int auto_increment primary key,
    user_id int not null,
    tag_id int not null,
    title varchar(50) not null,
    description varchar(500) not null,
    foreign key (tag_id) references Tags(tag_id),
    foreign key (user_id) references Users(user_id)
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

create table BlackListToken(
	token_id int auto_increment primary key,
    token varchar(500) not null,
    blacklisted_on datetime not null
);

-- drop table Comments;
-- drop table Preferences;
-- drop table Discussions;
-- drop table Tags;
-- drop table Users;
-- drop table Notifications;



-- dummy data
insert into Tags (tag_name) values 
                                ('UVT'),
                                ('UPT'),
                                ('UBB'),
                                ('UPB'),
                                ('UTCLUJ'),
                                ('UMFT'),
                                ('USAMVBT');

insert into Notifications (text, date) values 
                                ('notification1', '2019-01-01'),
                                ('notification2', '2019-01-02'),
                                ('notification3', '2019-01-03'),
                                ('notification4', '2019-01-04'),
                                ('notification5', '2019-01-05'),
                                ('notification6', '2019-01-06'),
                                ('notification7', '2019-01-07');

insert into Users (username, mail, password, name, last_notification_id) values 
                                ('user1', 'user1@mail.com', 'password1', 'name1', 1),
                                ('user2', 'user2@mail.com', 'password2', 'name2', 2),
                                ('user3', 'user3@mail.com', 'password3', 'name3', 3),
                                ('user4', 'user4@mail.com', 'password4', 'name4', 4),
                                ('user5', 'user5@mail.com', 'password5', 'name5', 5),
                                ('user6', 'user6@mail.com', 'password6', 'name6', 6),
                                ('user7', 'user7@mail.com', 'password7', 'name7', 7);

insert into Discussions (user_id, tag_id, title, description) values 
                                (1, 1, 'title1', 'description1'),
                                (2, 2, 'title2', 'description2'),
                                (3, 3, 'title3', 'description3'),
                                (4, 4, 'title4', 'description4'),
                                (5, 5, 'title5', 'description5'),
                                (6, 6,'title6', 'description6'),
                                (7, 7,'title7', 'description7');

insert into Preferences (user_id, tag_id) values 
                                (1, 1),
                                (2, 2),
                                (2, 3),
                                (3, 3),
                                (4, 4),
                                (5, 5),
                                (5, 1),
                                (5, 3),
                                (6, 6),
                                (7, 7),
                                (7, 6);

insert into Comments (user_id, discussion_id, date, text) values 
                                (1, 1, '2019-01-01', 'text1'),
                                (2, 1, '2019-01-02', 'text2'),
                                (3, 1, '2019-01-03', 'text3'),
                                (4, 1, '2019-01-04', 'text4'),
                                (5, 1, '2019-01-05', 'text5'),
                                (6, 1, '2019-01-06', 'text6'),
                                (7, 1, '2019-01-07', 'text7'),
                                (1, 2, '2019-01-01', 'text1'),
                                (2, 2, '2019-01-02', 'text2'),
                                (3, 2, '2019-01-03', 'text3'),
                                (4, 2, '2019-01-04', 'text4'),
                                (5, 2, '2019-01-05', 'text5'),
                                (6, 2, '2019-01-06', 'text6'),
                                (7, 2, '2019-01-07', 'text7'),
                                (1, 3, '2019-01-01', 'text1'),
                                (2, 3, '2019-01-02', 'text2'),
                                (3, 3, '2019-01-03', 'text3'),
                                (4, 3, '2019-01-04', 'text4'),
                                (5, 3, '2019-01-05', 'text5'),
                                (6, 3, '2019-01-06', 'text6'),
                                (7, 3, '2019-01-07', 'text7'),
                                (1, 4, '2019-01-01', 'text1'),
                                (2, 4, '2019-01-02', 'text2'),
                                (3, 4, '2019-01-03', 'text3'),
                                (4, 4, '2019-01-04', 'text4'),
                                (5, 4, '2019-01-05', 'text5'),
                                (6, 4, '2019-01-06', 'text6'),
                                (7, 4, '2019-01-07', 'text7'),
                                (1, 5, '2019-01-01', 'text1'),
                                (2, 5, '2019-01-02', 'text2'),
                                (3, 5, '2019-01-03', 'text3'),
                                (4, 5, '2019-01-04', 'text4'),
                                (5, 5, '2019-01-05', 'text5'),
                                (6, 5, '2019-01-06', 'text6'),
                                (7, 5, '2019-01-07', 'text7'),
                                (1, 6, '2019-01-01', 'text1'),
                                (2, 6, '2019-01-02', 'text2'),
                                (3, 6, '2019-01-03', 'text3'),
                                (4, 6, '2019-01-04', 'text4'),
                                (5, 6, '2019-01-05', 'text5'),
                                (6, 6, '2019-01-06', 'text6'),
                                (7, 6, '2019-01-07', 'text7'),
                                (1, 7, '2019-01-01', 'text1'),
                                (2, 7, '2019-01-02', 'text2'),
                                (3, 7, '2019-01-03', 'text3'),
                                (4, 7, '2019-01-04', 'text4'),
                                (5, 7, '2019-01-05', 'text5'),
                                (6, 7, '2019-01-06', 'text6'),
                                (7, 7, '2019-01-07', 'text7');

select * from blacklisttoken