import subprocess as pwsh



if __name__=="__main__":
    inpt=pwsh.run("powershell Read-Host",stdout=pwsh.PIPE).stdout.decode(errors="ignore").replace("\r","").replace("\n","")
    