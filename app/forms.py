from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CreateVM(FlaskForm):
    qcow2_size = StringField('Disk Size (qcow2)', validators=[DataRequired()])

    userdata_hostname = StringField('Hostname', validators=[DataRequired()])
    userdata_fqdn = StringField('FQDN', validators=[DataRequired()])
    userdata_user_name = StringField('User Name', validators=[DataRequired()])
    userdata_user_chpasswd = StringField('Password', validators=[DataRequired()])
    userdata_user_group = StringField('Groups', validators=[DataRequired()])
    userdata_user_ssh_key = StringField('SSH key', validators=[DataRequired()])
    userdata_sudo = BooleanField('Sudo privileges?')
    userdata_manage_etc_hosts = BooleanField('Manage /etc/hosts')
    userdata_expire = BooleanField('Expire?')
    userdata_disable_root = BooleanField('Disable root?')

    network_interface = StringField('Interface', validators=[DataRequired()])
    network_ipv4 = StringField('IPv4', validators=[DataRequired()])
    network_gw = StringField('Default Gateway', validators=[DataRequired()])
    network_ns1 = StringField('Nameserver 1', validators=[DataRequired()])
    network_ns2 = StringField('Nameserver 2', validators=[DataRequired()])
    network_search = StringField('Domain Search', validators=[DataRequired()])
    network_dhcp4 = BooleanField('Activate DHCP')
