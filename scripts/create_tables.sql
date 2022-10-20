drop database focusModeDBMS;
create database focusModeDBMS;
use focusModeDBMS;

create table SESSIONS (
	sessionID varchar(10) not null,
	sessionDate date not null,
	startTime time not null,
	endTime time not null,
	duration varchar(20),
	primary key (sessionID)
);

create table BREAKS (
	breakID varchar(10) not null,
	breakDate date not null,
	startTime time not null,
	endTime time not null,
	allowedDuration varchar(20) not null,
	sessionID varchar(10) not null,
	primary key (breakID),
	foreign key (sessionID) references SESSIONS(sessionID)
);

create table APPS (
	appID varchar(10) not null,
	appName varchar(50) not null,
	privileged bit not null,
	timer varchar(20),
	timerMAX varchar(20),
	primary key (appID)
);

create table WARNINGS (
	warningID varchar(10) not null,
	warningDate date not null,
	snooze varchar(20),
	appID varchar(10) not null,
	primary key (warningID),
	foreign key (appID) references APPS(appID)
);

create table SESSION_APPS (
	sessionID varchar(10) not null,
	appID varchar(10) not null,
	primary key (sessionID, appID)
);

create table BREAK_APPS (
	breakID varchar(10) not null,
	appID varchar(10) not null,
	primary key (breakID, appID)
);
