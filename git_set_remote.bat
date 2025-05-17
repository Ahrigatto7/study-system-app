@echo off
setlocal

:: 사용자 입력
set /p REPO_URL=🔗 Enter your GitHub repository URL (e.g. https://github.com/Ahrigatto7/repo.git): 
set /p COMMIT_MSG=📝 Enter commit message: 

:: 기존 origin 제거 시도
git remote remove origin 2>nul

:: 새 origin 설정
git remote add origin %REPO_URL%
echo ✅ Remote 'origin' set to: %REPO_URL%

:: 브랜치 설정 및 커밋/푸시
git branch -M main
git add .
git commit -m "%COMMIT_MSG%"
git push -u origin main

echo ✅ All done! Your code has been pushed to GitHub.
pause
endlocal
