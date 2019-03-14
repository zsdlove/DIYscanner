echo "正在启动极客扫描系统"
echo "please waite"
echo "..."

gnome-terminal -x bash -c "python ./geekbackend/manage.py runserver 0.0.0.0:8000"

gnome-terminal -x bash -c "cd ./PycharmProjects/DIYscanner&&python DBService.py"

gnome-terminal -x bash -c "cd ./PycharmProjects/DIYscanner&&python taskschedule.py"

gnome-terminal -x bash -c "cd ./PycharmProjects/DIYscanner&&celery -A scan worker -l info"

gnome-terminal -x bash -c "cd ./PycharmProjects/DIYscanner&&python mitm-startup.py"
echo "系统启动完毕"
