from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from .models import (
    Reporter, Issue, CriticalIssue, LowPriorityIssue
)
from .utils import (
    REPORTERS_FILE, ISSUES_FILE, read_json, write_json,
)

class ReporterView(APIView):

    def get(self, request):
        reporter_id = request.GET.get('id')
        reporters_data = read_json(
            REPORTERS_FILE
        )
        if reporter_id:
            try:
                reporter_id = int(reporter_id)
            except ValueError:
                return Response(
                    {'error': 'Invalid reporter ID'},
                    status=HTTP_400_BAD_REQUEST
                )

            for reporter in reporters_data:
                if reporter['id'] == reporter_id:
                    return Response(
                        reporter,
                        status=HTTP_200_OK
                    )

            return Response(
                {'error': 'Reporter not found'},
                status=404
            )
        return Response(
            reporters_data,
            status=HTTP_200_OK
        )

    def post(self, request):
        data = request.data

        try:
            reporter = Reporter(
                id=int(data['id']),
                name=data['name'],
                email=data['email'],
                team=data['team']
            )

            reporter.validate()

        except KeyError as e:
            return Response({'error': f'Missing field: {str(e)}'}, status=HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)

        reporters_data = read_json(
            REPORTERS_FILE
        )

        for existing_reporter in reporters_data:
            if existing_reporter['id'] == reporter.id:
                return Response(
                    {'error': 'Reporter ID already exists'},
                    status=HTTP_400_BAD_REQUEST
                )

        reporters_data.append(
            reporter.to_dict()
        )

        write_json(
            REPORTERS_FILE,
            reporters_data
        )

        return Response(
            reporter.to_dict(),
            status=HTTP_201_CREATED
        )


class IssueView(APIView):
    def get(self, request):
            issue_id = request.GET.get('id')
            issue_status = request.GET.get('status')

            issues_data = read_json(ISSUES_FILE)

            if issue_id:
                try:
                    issue_id = int(issue_id)
                except ValueError:
                    return Response(
                        {'error': 'Invalid issue ID'},
                        status=HTTP_400_BAD_REQUEST
                    )

                for issue in issues_data:

                    if issue['id'] == issue_id:

                        return Response(
                            issue,
                            status=HTTP_200_OK
                        )

                return Response(
                    {
                        'error': 'Issue not found'
                    },
                    status=404
                )

            if issue_status:
                filtered_issues = []
                for issue in issues_data:
                    if issue['status'] == issue_status:
                        filtered_issues.append(issue)
                return Response(
                    filtered_issues,
                    status=HTTP_200_OK
                )

            return Response(
                issues_data,
                status=HTTP_200_OK
            )
        
    def post(self, request):

        data = request.data

        try:
            reporters_data = read_json(REPORTERS_FILE)
            reporter_exists = False

            for reporter in reporters_data:
                if reporter['id'] == data['reporter_id']:
                    reporter_exists = True
                    break

            if not reporter_exists:
                return Response(
                    {'error': 'Reporter not found'},
                    status=404
                )

            if data['priority'] == 'critical':
                issue = CriticalIssue(
                    id=int(data['id']),
                    title=data['title'],
                    description=data['description'],
                    status=data['status'],
                    priority=data['priority'],
                    reporter_id=data['reporter_id']
                )
            elif data['priority'] == 'low':
                issue = LowPriorityIssue(
                    id=int(data['id']),
                    title=data['title'],
                    description=data['description'],
                    status=data['status'],
                    priority=data['priority'],
                    reporter_id=data['reporter_id']
                )
            else:
                issue = Issue(
                    id=int(data['id']),
                    title=data['title'],
                    description=data['description'],
                    status=data['status'],
                    priority=data['priority'],
                    reporter_id=data['reporter_id']
                )
            issue.validate()

        except KeyError as e:

            return Response(
                {'error': f'Missing field: {str(e)}'},
                status=HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=HTTP_400_BAD_REQUEST
            )

        issues_data = read_json(
            ISSUES_FILE
        )

        for existing_issue in issues_data:
            if existing_issue['id'] == issue.id:
                return Response(
                    {'error': 'Issue ID already exists'},
                    status=HTTP_400_BAD_REQUEST
                )

        issues_data.append(issue.to_dict())

        write_json(
            ISSUES_FILE,
            issues_data
        )

        response_data = issue.to_dict()
        response_data['message'] = issue.describe()

        return Response(
            response_data,
            status=HTTP_201_CREATED
        )

    