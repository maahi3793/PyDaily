import requests

url = "http://localhost:8000/api/v1/docs/upload"
file_path = r"c:\Users\reach\.gemini\antigravity\scratch\relaunchpython\dummy_crash_course.txt"

print("Uploading...")
with open(file_path, "rb") as f:
    files = {"file": (file_path.split("\\")[-1], f, "application/pdf")}
    data = {"chunk_size": 500, "chunk_overlap": 100}
    response = requests.post(url, files=files, data=data)

print(response.status_code)
print(response.json())
