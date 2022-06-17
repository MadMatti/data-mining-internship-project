CREATE VIEW log_difference AS
    SELECT l.id,
           l.user_id,
           l.userdisplayname,
           l.createdatetime as curr_time,
           lag(l.createdatetime) 
				over (partition by l.user_id order by l.createdatetime desc) as prec_time,
           lag(l.createdatetime) 
				over (partition by l.user_id order by l.createdatetime desc) - l.createdatetime as time_diff,
           l.latitude as curr_lat,
	       lag(l.latitude)
	   		    over (partition by l.user_id order by l.createdatetime desc) as prec_lat,
	       l.longitude as curr_long,
	       lag(l.longitude)
	   		    over (partition by l.user_id order by l.createdatetime desc) as prec_long,
           2*6317*asin(sqrt(power(sin(radians(l.latitude - lag(l.latitude) over (partition by l.user_id order by l.createdatetime desc))/2),2) 
		    + cos(radians(l.latitude))*cos(radians(lag(l.latitude) over(partition by l.user_id order by l.createdatetime desc))) 
		    * power(sin(radians(l.longitude - lag(l.longitude) over (partition by l.user_id order by l.createdatetime desc))/2),2))) as dist_diff
    FROM public.logs l