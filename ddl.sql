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

-- Ensure the `pgcrypto` extension is enabled for `gen_random_uuid()`
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- public.users definition
CREATE TABLE public.users (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    "name" varchar(100) NULL,
    email varchar(255) NOT NULL,
    "password" varchar NULL,
    birthdate date DEFAULT now() NOT NULL,
    upload_path varchar(100) NOT NULL,
    CONSTRAINT users_pk PRIMARY KEY (id)
);

-- public.files definition
CREATE TABLE public.files (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name varchar NOT NULL,
    category varchar NULL,
    user_id uuid NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT files_pk PRIMARY KEY (id),
    CONSTRAINT files_user_fk FOREIGN KEY (user_id) REFERENCES public.users (id) ON DELETE CASCADE
);

-- public.file_shares definition (for file sharing)
CREATE TABLE public.file_shares (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    file_id uuid NOT NULL,
    shared_by_id uuid NOT NULL,
    shared_with_id uuid NOT NULL,
    shared_at timestamp DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT file_shares_pk PRIMARY KEY (id),
    CONSTRAINT file_shares_file_fk FOREIGN KEY (file_id) REFERENCES public.files (id) ON DELETE CASCADE,
    CONSTRAINT file_shares_shared_by_fk FOREIGN KEY (shared_by_id) REFERENCES public.users (id) ON DELETE CASCADE,
    CONSTRAINT file_shares_shared_with_fk FOREIGN KEY (shared_with_id) REFERENCES public.users (id) ON DELETE CASCADE
);

-- Indexes for faster lookups on file shares
CREATE INDEX idx_file_shares_shared_by ON public.file_shares(shared_by_id);
CREATE INDEX idx_file_shares_shared_with ON public.file_shares(shared_with_id);
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