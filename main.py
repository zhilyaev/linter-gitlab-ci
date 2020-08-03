#!/usr/bin/python

import gitlab
import argparse
import re
import os

ERROR = '\033[31m'   # RED color
SUCCESS = '\033[34m'   # BLUE color
END = '\033[0m'
WARNING = '\033[33m'
WARNING_MESSAGE = 'jobs config should contain at least one visible job'


def linter(git_url, project_id, token, human_mask):
    file = None
    exit_code = 0
    try:
        gl = gitlab.Gitlab(url=git_url, private_token=token)
        project = gl.projects.get(project_id)
        # refactoring human_mask to RegExp:
        # 1) .      -> \\.
        # 2) **/*   -> [\\w\\./-]+ (this mask will matc files located anywhere in the project)
        # 3) *      -> [\\w\\.-]+ (this human_mask will match files located anywhere BUT in folders)
        re_mask = human_mask
        re_mask = list(map(lambda x: '^' + x, re_mask))
        re_mask = '|'.join(re_mask).replace('.', '\\.').replace('**/*', '[\\w\\./-]+').replace('*', '[\\w\\.-]+')
        # grab all files (in folders too) and apply filter human_mask to them;
        subdirs = [item.get('path') for item in project.repository_tree(recursive=True) if item.get('type') == 'tree']
        files_recursive = [item.get('path') for subdir in subdirs for item in project.repository_tree(path=subdir) 
                           if item.get('type') == 'blob' and re.search(re_mask, item.get('path'))]
        files_top = [item.get('path') for item in project.repository_tree() if item.get('type') == 'blob' 
                     and re.search(re_mask, item.get('path'))]

        files = files_top + files_recursive
        if not files:
            print(f"{ERROR}Files matching {human_mask} not found in {git_url}/{project.path_with_namespace}{END}")
            return exit(1)

        for file in files:
            f = project.files.get(file_path=file, ref='master').decode().decode('utf-8')
            res = gl.lint(f)
            # print lint message (valid or error)
            if res[0] or re.match('[\\w\\.\\/-]+-task\\.yml', file) and res[1][0] == WARNING_MESSAGE:
                # OK
                print(f"{file} — {SUCCESS if res[0] else WARNING}{'Syntax is correct' if res[0] else res[1][0]}{END}")

            else:
                # NOT OK :(
                print(f"{file} — {ERROR}{res[1][0]}{END}")
                exit_code = 1

        return exit(exit_code)

    # catching decode() - file exists but it is empty
    # catching Exception - can't locate project, probably because of invalid id, host url or token
    except (UnicodeDecodeError, Exception):
        if file:
            print(f"{ERROR}Something went wrong with Unicode Decoder on file{END} {file}."
                  f"{ERROR} File might be empty. Try to change filter human_mask{END}")
        else:
            print(f"{ERROR}Project not found! \nCheck carefully your PROJECT ID ({project_id}), "
                  f"URL ({git_url}) and ACCESS TOKEN ({'Hidden' if token else 'None'}){END}")
        return exit(1)


def parser_args():
    parser = argparse.ArgumentParser(description='Linter gitlab-ci')

    parser.add_argument('-u', '--url',
                        type=str,
                        action='store',
                        default=os.getenv('GITLAB_LINT_API', 'https://gitlab.com'),
                        help='Set your host URL')

    parser.add_argument('-id',
                        type=int,
                        action='store',
                        default=os.getenv('GITLAB_LINT_PROJECT_ID', 11),
                        help='Set your project id')

    parser.add_argument('-t', '--token',
                        type=str,
                        action='store',
                        default=os.getenv('GITLAB_LINT_ACCESS_TOKEN', None),
                        help='Set your access token')

    parser.add_argument('-m', '--human_mask',
                        type=str,
                        nargs='*',
                        action='store',
                        default=os.getenv('GITLAB_LINT_FILE', '*.yml').split(' '),
                        help='Set human_mask of files')

    return parser.parse_args()


def main():
    args = parser_args()
    token = args.token
    human_mask = args.human_mask
    project_id = args.id
    project_host = args.url

    print(linter(project_host, project_id, token, human_mask))


if __name__ == '__main__':
    main()
