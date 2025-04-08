from kombu import Exchange, Queue

# Broker settings
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

# Task settings
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

# Queue settings
task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('instagram', Exchange('instagram'), routing_key='instagram'),
)

task_routes = {
    'app.tasks.instagram_tasks.*': {'queue': 'instagram'},
}

# Task execution settings
task_acks_late = True
task_reject_on_worker_lost = True
task_track_started = True

# Worker settings
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1000

# Beat settings
beat_schedule = {
    'cleanup-old-media': {
        'task': 'app.tasks.instagram_tasks.cleanup_old_media',
        'schedule': 86400.0,  # Run once per day
    },
} 