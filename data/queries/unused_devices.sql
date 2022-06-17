SELECT d.device_id, d.displayname
FROM public.devices d
LEFT JOIN public.logs l
    on d.device_id = l.device_id
WHERE l.id is NULL