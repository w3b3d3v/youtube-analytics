import functions_framework
import videos

@functions_framework.http
def update_youtube_data(request):
    videos.run()
    return 'OK'
