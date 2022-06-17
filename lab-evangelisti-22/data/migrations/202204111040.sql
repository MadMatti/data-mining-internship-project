DROP VIEW IF EXISTS log_difference;

CREATE MATERIALIZED VIEW log_difference
AS
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
	   		    over prec as prec_long,
           2*6317*asin(sqrt(power(sin(radians(l.latitude - lag(l.latitude) over prec)/2),2) 
		    + cos(radians(l.latitude))*cos(radians(lag(l.latitude) over prec)) 
		    * power(sin(radians(l.longitude - lag(l.longitude) over prec)/2),2))) as dist_diff
    FROM public.logs l
        WINDOW prec AS (partition by l.user_id order by l.createdatetime desc)
WITH DATA