import functions_framework
import videos

@functions_framework.http
def update_youtube_data(request):
    ok = videos.run()
    return 'OK' if ok else 'NOT OK'
