from typing import Dict

from ..common.icons import Icons, Icon
from ..pull_requests import PullRequestStatus


class BitbucketIcons(object):
    BITBUCKET = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAOCAYAAAAmL5yKAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAOxAAADsQBlSsOGwAAActpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+d3d3Lmlua3NjYXBlLm9yZzwveG1wOkNyZWF0b3JUb29sPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KGMtVWAAAAjVJREFUKBWFU8tqVEEQPVXdfe9NHBKU4FvBLARFA+78EtEfEP8hm1mo/yCuXPgN2blz4UpcaIyTBBIxIEExcTJM7u3u8vSdKLqyhurbj6pzqk/1yPXHtgbDLQjGBjgBV/+3yJBF+lvP4ZJfxOU0AdRx9TudSP/YX/uWyHQKiAfY94x7nVvctsgKEuoTAIaALMZj6VPNrMT2FNyImMi8CN54LkY9M1AxKdBNAoLOZrMimGlRQILMDS1AjtEpYdvz7utkL8SOXCYKyR1G9I8MbMhs4qRN0+ObKdqyWRcZ7GXSALnb8ITbyseILMfzoNWalUzxamNVHs3oZ6Pee/fCwsKyHe23EMfY1PJCm+pa7DHkixY5iWks0gx3+hUFKDcq3sw1K3Xl4OtapGogql/PNPmzvh/KmMFbQgBG5qIwbfnGE7vArw2HkKWHO+d9Fa55NYS61lDPwVVh5/vLu4daosmxAc6ogxQA6rCUDFfK2XAoOXp/LjQLi07NXAjqWYH31aicnxSO9ZJNc/xSNUiK8fnV1aPdnJKmrruYi/5VgETVzBZYDutTbvUATvGJqhcrrcwFzNV+RemRHdLjhDj9aahqUek0U/lcNx9KQg8gGdsEGFOEAZP7NhEmlra6XO7ERxAqFY1IQowUW6lk8w9AaLDHpvxw8xjwSVdS3huJy+C8g1J9x0piTGR06CYHhxrP7pZzCj8z/qmecXaf/o0+08ZOzvkI+ZOUU8xdPJ1zXNt5OniAoekvT/f0vYI/tMoAAAAASUVORK5CYII=")

    PULL_REQUEST = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAVCAYAAABPPm7SAAAAAXNSR0IArs4c6QAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAbVJREFUOBGNlD0ohVEYxw/XZ4muiZHFbMFgllLKJKuFYlAWm0ExKCmT3WBS7qyLO8soE5uPRVEGHxf/33H+b++te+Nfv/s85/l6zznvvTeE+mpWuC2lpmSnk0+sKfk1ZlGritgTxVxmTP63mMnFcAv59ZYWFJXEm7gRaFx8CXK7YlZMCCsbQsFqig7I0rQvXgQ5hmLNpfxBgQqclUQ/K6lPcMY78SzqaVjBU9ElqhQsCYaUBU87E2hIPAly64LGA+FjrcnPdCSPQrZdzKIh+EhzKdYr66GHxFpS4jVZBvg1dci/FSPCQ6lnl4gHZgM8COsB7yl/QWESZ+beMnkRpymKtU/Rp6DGryyfiw/yAIobyZdWN/+fAXUbHfQAnxtr3zV563piNUf4SFWcmS03EjlqULSe2P0bCz2yvrD8TuxjXcs3MWpFn9xuWfDqzkVebiZ2Iqihlp5lEZ1tHIkvDYlJFlKr8I74JZIbFYieqo/wGEMhPCTbnizGO+hMsftkqY39G3KYXBJs70q4CeuHsJNrwYUfC3o2RdS8PjnXjvAluZEC+/wm+NeqiAUR5ad5jXXDX7HwA+nmXWV5F/zGAAAAAElFTkSuQmCC")

    PR_STATUSES: Dict[PullRequestStatus, Icon] = {
        PullRequestStatus.UNAPPROVED: Icons.GREY_CIRCLE,
        PullRequestStatus.NEEDS_WORK: Icons.ORANGE_CIRCLE,
        PullRequestStatus.APPROVED: Icons.GREEN_CIRCLE
    }
