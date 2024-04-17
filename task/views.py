from rest_framework.views import APIView
from rest_framework.response import Response


class CheckTaskValidation(APIView):
    def post(self, request):
        tasks = request.data.get("tasks", [])
        if not tasks:
            return Response("No tasks provided", status=400)

        task_dict = {task["id"]: task for task in tasks}

        for task in tasks:
            pre_task_ids = task.get("pre_tasks", [])
            task_time = task.get("time_to_send")

            for pre_task_id in pre_task_ids:
                pre_task = task_dict.get(pre_task_id)
                if pre_task and pre_task.get("time_to_send") >= task_time:
                    return Response("No")

        return Response("Yes")
