DROP VIEW IF EXISTS log_difference;

CREATE VIEW log_difference AS
    SELECT l.id,
           l.user_id,
           l.userdisplayname,
           l.createdatetime as curr_time,
           lag(l.createdatetime) 
				over prec as prec_time,
           lag(l.createdatetime) 
				over prec - l.createdatetime as time_diff,
           l.latitude as curr_lat,
	       lag(l.latitude)
	   		    over prec as prec_lat,
	       l.longitude as curr_long,
	       lag(l.longitude)
	   		    over prec as prec_long
    FROM public.logs l 
        WINDOW prec AS (partition by l.user_id order by l.createdatetime desc)