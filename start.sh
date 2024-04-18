if [ -z $SOURCE_CODE ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Nisarg7021/TG-URL-Shortener-Bot.git /TG-URL-Shortener-Bot
else
  echo "Cloning Custom Repo from $SOURCE_CODE "
  git clone $SOURCE_CODE /TG-URL-Shortener-Bot
fi
cd /TG-URL-Shortener-Bot
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 -m main
