ALTER TABLE public.logs
ADD COLUMN city text,
ADD COLUMN state text,
ADD COLUMN altitude double precision,
ADD COLUMN latitude double precision,
ADD COLUMN longitude double precision;