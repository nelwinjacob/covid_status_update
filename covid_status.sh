#PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/nelwinjacob/Coding/DSA/covid_script/bin/
#source /home/nelwinjacob/Coding/DSA/covid_script/bin/activate
now=$(date +"%d-%m-%Y-%H-%M-%S-%3N")
formatted_time=$(date +"%d-%m-%Y %r")
echo "Current time : ${now}"
filename="covid_stats_${now}"
x=($(python /home/nelwinjacob/Development/covid_status/covid_data_scraper.py))
ret=$?
if [ $ret -ne 0 ]
then
    echo "ERROR: Unable to fetch data from Internet. Check your internet connection."
else
    echo "Filename: ${filename}.txt"
    echo -e "Corona Virus Update: ${formatted_time}" > /home/nelwinjacob/Development/"${filename}".txt
    echo "World Total Cases: ${x[0]}"  >> /home/nelwinjacob/Development/"${filename}".txt
    echo "World New Cases: ${x[1]}"  >> /home/nelwinjacob/Development/"${filename}".txt
    echo "India Total Cases: ${x[2]}"  >> /home/nelwinjacob/Development/"${filename}".txt
    echo "India New Cases: ${x[3]}"  >> /home/nelwinjacob/Development/"${filename}".txt
fi