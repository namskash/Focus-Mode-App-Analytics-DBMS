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
	breakDuration varchar(20) not null,
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

/*
create table WARNINGS (
	warningID varchar(10) not null,
	warningDate date not null,
	snooze varchar(20),
	appID varchar(10) not null,
	primary key (warningID),
	foreign key (appID) references APPS(appID)
);
*/

create table SESSION_APPS (
	sessionID varchar(10) not null,
	appID varchar(10) not null,
	primary key (sessionID, appID),
	foreign key (sessionID) references SESSIONS (sessionID),
	foreign key (appID) references APPS (appID)
);

create table BREAK_APPS (
	breakID varchar(10) not null,
	appID varchar(10) not null,
	primary key (breakID, appID),
	foreign key (breakID) references BREAKS (breakID),
	foreign key (appID) references APPS (appID)
);

/*
delimiter &&  
create procedure getNEntries (in lim int)  
begin  
    select * from APPS limit lim;  
end &&  
delimiter; 


delimiter $$  
create function appType(privileged int)
returns varchar(20)
deterministic
begin
    declare typeOfApp varchar(20);
    if privileged > 0 then
        set typeOfApp = 'privileged';

    elseif privileged < 1 then
        set typeOfApp = 'non-privileged';

    end if;

    return (typeOfApp);
end $$
delimiter

create trigger sumDuration before insert on BREAKS
    for each row set @sum = @sum + NEW.breakDuration;
*/
