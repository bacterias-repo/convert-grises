import os
import cv2
import requests
from github import Github

def convert_to_gray(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def upload_to_github(image_path, repo_name, repo_branch, github_token):
    g = Github(github_token)
    user = g.get_user()
    repo = user.get_repo(repo_name)
    branch = repo.get_branch(repo_branch)
    file_path = os.path.basename(image_path)
    with open(image_path, 'rb') as file:
        content = file.read()
    repo.create_file(file_path, f'Added {file_path}', content, branch=branch.name)
    return f'Image uploaded to {repo_name} repository in {repo_branch} branch.'

def convert_to_grayscale(event):
    image_url = event['body-json']['image_url']
    github_token = event['headers']['x-github-token']
    repo_name = event['headers']['x-github-repo']
    repo_branch = event['headers']['x-github-branch']
    image_filename = os.path.basename(image_url)
    image_response = requests.get(image_url)
    image_path = f'/tmp/{image_filename}'
    with open(image_path, 'wb') as file:
        file.write(image_response.content)
    gray_image = convert_to_gray(image_path)
    cv2.imwrite(image_path, gray_image)
    upload_to_github(image_path, repo_name, repo_branch, github_token)
    return f'Image {image_filename} converted to grayscale and uploaded to GitHub repository.'

