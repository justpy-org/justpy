from github import Github

# https://pygithub.readthedocs.io/en/latest/examples/Repository.html#get-all-of-the-contents-of-the-root-directory-of-the-repository


def list_repos():
    g = Github("elimintz", "g89$#78FkGH")
    for repo in g.get_user().get_repos():
        print(repo.name)
        contents = repo.get_contents("")
        while len(contents) > 0:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                print(file_content)


list_repos()