-- public.doctors definition

-- Drop table

-- DROP TABLE public.doctors;

CREATE TABLE public.doctors (
	id uuid NOT NULL,
	"name" varchar NOT NULL,
	email varchar NOT NULL,
	phone varchar NOT NULL,
	specialty varchar NULL,
	hospital varchar NULL,
	CONSTRAINT doctors_pk PRIMARY KEY (id)
);


-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	id uuid NOT NULL,
	"name" varchar(100) NULL,
	email varchar(255) NOT NULL,
	"password" varchar NULL,
	birthdate date DEFAULT now() NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
);


-- public.hospitals definition

-- Drop table

-- DROP TABLE public.hospitals;

CREATE TABLE public.hospitals (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	"name" varchar(255) NOT NULL,
	"location" varchar(128) NOT NULL,
	CONSTRAINT hospitals_pk PRIMARY KEY (id)
);


-- public.insurances definition

-- Drop table

-- DROP TABLE public.insurances;

CREATE TABLE public.insurances (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT insurances_pk PRIMARY KEY (id)
);


-- public.examinations definition

-- Drop table

-- DROP TABLE public.examinations;

CREATE TABLE public.examinations (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	"name" varchar(255) NULL,
	hospital_id uuid NULL,
	user_id uuid NULL,
	"date" date DEFAULT now() NOT NULL,
	CONSTRAINT examinations_pk PRIMARY KEY (id)
);


-- public.appointments definition

-- Drop table

-- DROP TABLE public.appointments;

CREATE TABLE public.appointments (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	reason varchar(255) NULL,
	"date" date DEFAULT now() NOT NULL,
	user_id uuid NOT NULL,
	doctor_id uuid NOT NULL,
	pending bool DEFAULT true NOT NULL,
	hospital_id uuid NULL,
	heart_rate varchar(128) NULL,
	blood_pressure varchar NULL,
	weight numeric NULL,
	recommendations varchar(255) NULL,
	CONSTRAINT appointments_pk PRIMARY KEY (id),
	CONSTRAINT appointments_doctors_fk FOREIGN KEY (doctor_id) REFERENCES public.doctors(id),
	CONSTRAINT appointments_hospitals_fk FOREIGN KEY (hospital_id) REFERENCES public.hospitals(id),
	CONSTRAINT appointments_users_fk FOREIGN KEY (user_id) REFERENCES public.users(id)
);


-- public.subscriptions definition

-- Drop table

-- DROP TABLE public.subscriptions;

CREATE TABLE public.subscriptions (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	"plan" varchar(128) NOT NULL,
	start_date date DEFAULT now() NULL,
	active bool DEFAULT true NOT NULL,
	user_id uuid NULL,
	insurance_id uuid NULL,
	CONSTRAINT subscriptions_pk PRIMARY KEY (id),
	CONSTRAINT subscriptions_insurances_fk FOREIGN KEY (insurance_id) REFERENCES public.insurances(id),
	CONSTRAINT subscriptions_users_fk FOREIGN KEY (user_id) REFERENCES public.users(id)
);


-- public.medications definition

-- Drop table

-- DROP TABLE public.medications;

CREATE TABLE public.medications (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	"name" varchar NOT NULL,
	active bool DEFAULT true NOT NULL,
	schedule varchar NOT NULL,
	appointment_id uuid NULL,
	user_id uuid NULL,
	CONSTRAINT medications_pk PRIMARY KEY (id),
	CONSTRAINT medications_appointments_fk FOREIGN KEY (appointment_id) REFERENCES public.appointments(id)
);