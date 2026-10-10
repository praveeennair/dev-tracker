def validate_reporter(data):
    if not data.get('name'):
        raise ValueError('Name cannot be empty')

    if '@' not in data.get('email', ''):
        raise ValueError('Invalid email')


def validate_issue(data):
    if not data.get('title'):
        raise ValueError('Title cannot be empty')

    allowed_statuses = [
        'open',
        'in_progress',
        'resolved',
        'closed'
    ]

    allowed_priorities = [
        'low',
        'medium',
        'high',
        'critical'
    ]

    if data.get('status') not in allowed_statuses:
        raise ValueError('Invalid status')

    if data.get('priority') not in allowed_priorities:
        raise ValueError('Invalid priority')
