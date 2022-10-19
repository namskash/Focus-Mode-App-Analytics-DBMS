drop database focusModeDBMS;
create database focusModeDBMS;
use focusModeDBMS;

create table SESSIONS (
	sessionID int not null,
	sessionDate date not null,
	startTime time not null,
	endTime time not null,
	duration varchar(20),
	primary key (sessionID)
);

create table BREAKS (
	breakID int not null,
	breakDate date not null,
	startTime time not null,
	endTime time not null,
	allowedDuration varchar(20) not null,
	sessionID int not null,
	primary key (breakID),
	foreign key (sessionID) references SESSIONS(sessionID)
);

create table APPS (
	appID int not null,
	privileged bit not null,
	timer varchar(20),
	timerMAX varchar(20),
	primary key (appID)
);

create table WARNINGS (
	warningID int not null,
	warningDate date not null,
	snooze varchar(20),
	appID int not null,
	primary key (warningID),
	foreign key (appID) references APPS(appID)
);

create table SESSION_APPS (
	sessionID int not null,
	appID int not null,
	primary key (sessionID, appID)
);

create table BREAK_APPS (
	breakID int not null,
	appID int not null,
	primary key (breakID, appID)
);