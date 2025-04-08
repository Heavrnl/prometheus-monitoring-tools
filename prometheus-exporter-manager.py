#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import sys
import re
import yaml
import shutil
import subprocess
from datetime import datetime

# 配置文件路径
CONFIG_FILE = "/root/docker/Grafana/prometheus.yml"
MY_VPS_FILE = "/root/docker/Grafana/prometheus-data/blackbox/my_vps.yml"
MY_VPS_V6_FILE = "/root/docker/Grafana/prometheus-data/blackbox/my_vps_v6.yml"

def validate_ip(ip, allow_ipv6=False):
    """验证IP地址格式是否正确"""
    # IPv4验证
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$'

    # IPv6验证
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^([0-9a-fA-F]{1,4}:){1,7}:|^:((:[0-9a-fA-F]{1,4}){1,7}|:)$|^[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})$|^([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}$|^([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}$|^([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}$|^([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}$|^([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}$'

    if re.match(ipv4_pattern, ip):
        # 验证IPv4地址各部分的数值范围
        if ':' in ip:
            ip_part = ip.split(':')[0]
        else:
            ip_part = ip

        parts = ip_part.split('.')
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    elif allow_ipv6 and re.match(ipv6_pattern, ip):
        return True
    return False

def load_config():
    """加载Prometheus配置文件"""
    if not os.path.exists(CONFIG_FILE):
        print(f"错误: 配置文件 {CONFIG_FILE} 不存在!")
        sys.exit(1)

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"加载配置文件失败: {str(e)}")
        sys.exit(1)

def load_my_vps():
    """加载my_vps.yml文件"""
    if not os.path.exists(MY_VPS_FILE):
        print(f"警告: 文件 {MY_VPS_FILE} 不存在，将创建新文件。")
        return []

    try:
        with open(MY_VPS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return []
            vps_config = yaml.safe_load(content)
            if not vps_config:
                return []
            return vps_config
    except Exception as e:
        print(f"加载my_vps文件失败: {str(e)}")
        return []

def load_my_vps_v6():
    """加载my_vps_v6.yml文件"""
    if not os.path.exists(MY_VPS_V6_FILE):
        print(f"警告: 文件 {MY_VPS_V6_FILE} 不存在，将创建新文件。")
        return []

    try:
        with open(MY_VPS_V6_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return []
            vps_config = yaml.safe_load(content)
            if not vps_config:
                return []
            return vps_config
    except Exception as e:
        print(f"加载my_vps_v6文件失败: {str(e)}")
        return []

def save_config(config):
    """保存Prometheus配置文件"""
    # 创建备份
    backup_file = f"{CONFIG_FILE}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    try:
        shutil.copy2(CONFIG_FILE, backup_file)
        print(f"已创建配置文件备份: {backup_file}")

        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return True
    except Exception as e:
        print(f"保存配置文件失败: {str(e)}")
        return False

def save_my_vps(vps_config):
    """保存my_vps.yml文件"""
    # 创建备份
    if os.path.exists(MY_VPS_FILE):
        backup_file = f"{MY_VPS_FILE}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        try:
            shutil.copy2(MY_VPS_FILE, backup_file)
            print(f"已创建my_vps文件备份: {backup_file}")
        except Exception as e:
            print(f"创建my_vps备份失败: {str(e)}")

    try:
        with open(MY_VPS_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(vps_config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return True
    except Exception as e:
        print(f"保存my_vps文件失败: {str(e)}")
        return False

def save_my_vps_v6(vps_config):
    """保存my_vps_v6.yml文件"""
    # 创建备份
    if os.path.exists(MY_VPS_V6_FILE):
        backup_file = f"{MY_VPS_V6_FILE}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        try:
            shutil.copy2(MY_VPS_V6_FILE, backup_file)
            print(f"已创建my_vps_v6文件备份: {backup_file}")
        except Exception as e:
            print(f"创建my_vps_v6备份失败: {str(e)}")

    try:
        with open(MY_VPS_V6_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(vps_config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return True
    except Exception as e:
        print(f"保存my_vps_v6文件失败: {str(e)}")
        return False

def format_instance_to_name(instance_name):
    """将实例名称格式化为name标签格式
    例如：HK-Alice -> 'HK | Alice'
    """
    if '-' in instance_name:
        parts = instance_name.split('-', 1)
        return f"{parts[0]} | {parts[1]}"
    return instance_name

def restart_prometheus():
    """重启Prometheus容器"""
    try:
        print("正在重启Prometheus容器...")
        result = subprocess.run(["docker", "restart", "prometheus"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Prometheus容器重启成功。")
            return True
        else:
            print(f"重启失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"重启Prometheus容器时出错: {str(e)}")
        return False

def remove_target(config, target_ip):
    """从配置中删除特定IP的目标"""
    changes_made = False
    instance_name = None

    # 如果没有提供端口，添加默认端口9100进行搜索
    base_ip = target_ip
    if ':' not in target_ip:
        target_ip_with_port = f"{target_ip}:9100"
    else:
        target_ip_with_port = target_ip
        base_ip = target_ip.split(':')[0]

    # 1. 在prometheus job中移除target
    for job in config.get('scrape_configs', []):
        if job.get('job_name') == 'prometheus':
            static_configs = job.get('static_configs', [])
            new_static_configs = []

            for static_config in static_configs:
                targets = static_config.get('targets', [])
                # 检查targets中是否包含目标IP
                if any(target_ip_with_port in target for target in targets):
                    # 记录实例名称，用于后续删除my_vps中的条目
                    instance_name = static_config.get('labels', {}).get('instance')
                    changes_made = True
                    continue
                new_static_configs.append(static_config)

            if len(new_static_configs) != len(static_configs):
                job['static_configs'] = new_static_configs

    # 2. 移除包含目标IP作为replacement的job (排除cadvisor)
    new_scrape_configs = []
    for job in config.get('scrape_configs', []):
        job_name = job.get('job_name', '')

        # 保留prometheus和cadvisor job
        if job_name in ['prometheus', 'cadvisor']:
            new_scrape_configs.append(job)
            continue

        # 处理blackbox_exporter job
        if job_name == 'blackbox_exporter':
            # 检查static_configs中是否包含目标IP
            static_configs = job.get('static_configs', [])
            new_static_configs = []

            for static_config in static_configs:
                targets = static_config.get('targets', [])
                new_targets = []

                for target in targets:
                    if base_ip not in target:
                        new_targets.append(target)
                    else:
                        changes_made = True
                        print(f"已从 blackbox_exporter job 中移除IP为 {base_ip} 的目标")

                if new_targets:
                    static_config['targets'] = new_targets
                    new_static_configs.append(static_config)

            # 如果还有其他目标，保留这个job，否则删除
            if new_static_configs:
                job['static_configs'] = new_static_configs
                new_scrape_configs.append(job)
            else:
                changes_made = True
                print(f"已删除空的 blackbox_exporter job")
            continue

        # 检查其他job的replacement字段
        relabel_configs = job.get('relabel_configs', [])
        should_remove = False

        for relabel in relabel_configs:
            if relabel.get('target_label') == '__address__' and base_ip in relabel.get('replacement', ''):
                should_remove = True
                changes_made = True
                # 如果没有记录实例名称，使用job名称
                if not instance_name:
                    instance_name = job_name
                break

        if not should_remove:
            new_scrape_configs.append(job)

    if len(new_scrape_configs) != len(config.get('scrape_configs', [])):
        config['scrape_configs'] = new_scrape_configs

    # 3. 从my_vps文件中删除条目
    vps_config = load_my_vps()
    if vps_config:
        new_vps_config = []
        for item in vps_config:
            targets = item.get('targets', [])
            if targets and base_ip in targets[0]:
                changes_made = True
                continue
            new_vps_config.append(item)

        if len(new_vps_config) != len(vps_config):
            save_my_vps(new_vps_config)
            print(f"已从my_vps.yml中删除IP为 {base_ip} 的目标。")

    # 4. 从my_vps_v6文件中删除可能的IPv6条目
    if instance_name:
        vps_v6_config = load_my_vps_v6()
        if vps_v6_config:
            formatted_name = format_instance_to_name(instance_name)
            new_vps_v6_config = []
            for item in vps_v6_config:
                labels = item.get('labels', {})
                if labels and labels.get('name') == formatted_name:
                    changes_made = True
                    continue
                new_vps_v6_config.append(item)

            if len(new_vps_v6_config) != len(vps_v6_config):
                save_my_vps_v6(new_vps_v6_config)
                print(f"已从my_vps_v6.yml中删除实例名为 {formatted_name} 的目标。")

    return changes_made

def add_target(config, target_ip, instance_name, code, city, filter_ipv6=False, ipv6_address=None, basic_auth_username=None, basic_auth_password=None):
    """添加监控目标到配置中

    参数:
        config: Prometheus配置字典
        target_ip: 目标IP地址
        instance_name: 实例名称
        code: 机场代码
        city: 城市名称
        filter_ipv6: 是否过滤IPv6，True表示添加IPv6过滤规则
        ipv6_address: IPv6地址，如果提供则添加到my_vps_v6.yml
        basic_auth_username: Basic认证用户名
        basic_auth_password: Basic认证密码
    """
    changes_made = False

    # 如果没有提供端口，添加默认端口9100
    if ':' not in target_ip:
        target_ip_with_port = f"{target_ip}:9100"
    else:
        target_ip_with_port = target_ip
        target_ip = target_ip.split(':')[0]

    # 1. 添加到prometheus job的static_configs中
    for job in config.get('scrape_configs', []):
        if job.get('job_name') == 'prometheus':
            if 'static_configs' not in job:
                job['static_configs'] = []

            # 检查是否已存在相同的目标
            exists = False
            for static_config in job.get('static_configs', []):
                if any(target_ip_with_port in target for target in static_config.get('targets', [])):
                    exists = True
                    break

            if not exists:
                # 添加新的监控目标
                job['static_configs'].append({
                    'targets': [target_ip_with_port],
                    'labels': {
                        'instance': instance_name
                    }
                })
                changes_made = True
                break

    # 2. 添加新的job用于blackbox监控
    port = '9115'  # 默认blackbox_exporter端口
    new_job = {
        'job_name': instance_name,
        'metrics_path': '/probe',
        'params': {
            'module': ['icmp']
        },
        'file_sd_configs': [{
            'files': ['/etc/prometheus/blackbox/*.yml']
        }],
        'relabel_configs': [
            {
                'source_labels': ['__address__'],
                'target_label': '__param_target'
            },
            {
                'source_labels': ['__param_target'],
                'target_label': 'instance'
            },
            {
                'target_label': '__address__',
                'replacement': f"{target_ip}:{port}"
            }
        ]
    }

    # 3. 如果提供了Basic认证信息，添加一个新的job来监控blackbox_exporter的metrics端点
    if basic_auth_username and basic_auth_password:
        # 检查是否已存在blackbox_exporter的metrics job
        blackbox_metrics_job_exists = False
        for job in config.get('scrape_configs', []):
            if job.get('job_name') == 'blackbox_exporter':
                # 更新现有job的basic_auth配置
                job['basic_auth'] = {
                    'username': basic_auth_username,
                    'password': basic_auth_password
                }
                blackbox_metrics_job_exists = True
                break

        # 如果不存在，创建新的job
        if not blackbox_metrics_job_exists:
            blackbox_metrics_job = {
                'job_name': 'blackbox_exporter',
                'metrics_path': '/metrics',
                'static_configs': [{
                    'targets': [f"{target_ip}:{port}"]
                }],
                'basic_auth': {
                    'username': basic_auth_username,
                    'password': basic_auth_password
                }
            }
            config['scrape_configs'].append(blackbox_metrics_job)
            print(f"已添加blackbox_exporter metrics端点的Basic认证配置")

        # 在新job中添加basic_auth配置
        # 注意：这里不需要添加，因为在检查已存在job时会添加

    # 如果需要过滤IPv6，添加过滤配置
    if filter_ipv6:
        new_job['relabel_configs'].append({
            'source_labels': ['ip'],
            'regex': 'IPv6',
            'action': 'drop'
        })

    # 检查是否已存在相同名称的job
    exists = False
    for job in config.get('scrape_configs', []):
        if job.get('job_name') == instance_name:
            exists = True
            # 如果已存在且提供了Basic认证信息，更新认证配置
            if basic_auth_username and basic_auth_password:
                job['basic_auth'] = {
                    'username': basic_auth_username,
                    'password': basic_auth_password
                }
                print(f"已更新{instance_name}的Basic认证配置")
            break

    if not exists:
        # 如果提供了Basic认证信息，添加到job配置中
        if basic_auth_username and basic_auth_password:
            new_job['basic_auth'] = {
                'username': basic_auth_username,
                'password': basic_auth_password
            }
        config['scrape_configs'].append(new_job)
        changes_made = True
        print(f"已添加{instance_name}格式的job")

    # 3. 添加到my_vps.yml
    vps_config = load_my_vps()
    formatted_name = format_instance_to_name(instance_name)

    # 检查是否已存在
    exists = False
    for item in vps_config:
        if item.get('targets') and target_ip in item.get('targets')[0]:
            exists = True
            break

    if not exists:
        vps_entry = {
            'targets': [target_ip],
            'labels': {
                'name': formatted_name,
                'code': code,
                'city': city,
                'ip': 'IPv4'
            }
        }
        vps_config.append(vps_entry)
        save_my_vps(vps_config)
        print(f"已将IPv4目标添加到my_vps.yml")

    # 4. 添加到my_vps_v6.yml
    if ipv6_address:
        vps_v6_config = load_my_vps_v6()

        # 检查是否已存在
        exists = False
        for item in vps_v6_config:
            if item.get('labels', {}).get('name') == formatted_name:
                exists = True
                break

        if not exists:
            vps_v6_entry = {
                'targets': [ipv6_address],
                'labels': {
                    'name': formatted_name,
                    'code': code,
                    'city': city,
                    'ip': 'IPv6'
                }
            }
            vps_v6_config.append(vps_v6_entry)
            save_my_vps_v6(vps_v6_config)
            print(f"已将IPv6目标添加到my_vps_v6.yml")

    return changes_made

def main():
    """主函数"""
    while True:
        print("\nPrometheus监控目标管理工具")
        print("=========================")
        print("1. 添加监控目标")
        print("2. 删除监控目标")
        print("3. 退出")

        choice = input("\n请选择操作 [1-3]: ")

        if choice == '1':
            target_ip = input("请输入要添加的被控端IP地址 (例如: 192.168.1.1): ")
            if not validate_ip(target_ip):
                print("错误: 请输入有效的IPv4地址格式 (例如: 192.168.1.1)")
                input("按Enter键继续...")
                continue

            instance_name = input("请输入实例名称 (例如: HK-Alice): ")
            if not instance_name:
                print("错误: 实例名称不能为空")
                input("按Enter键继续...")
                continue

            code = input("请输入机场代码 (例如: HKG): ")
            if not code:
                print("错误: 机场代码不能为空")
                input("按Enter键继续...")
                continue

            city = input("请输入城市名称 (例如: Hong Kong): ")
            if not city:
                print("错误: 城市名称不能为空")
                input("按Enter键继续...")
                continue

            need_ipv6 = input("是否需要监听IPv6? (y/n): ").lower() == 'y'
            # 如果不需要监听IPv6，则添加过滤
            filter_ipv6 = not need_ipv6
            ipv6_address = None

            # 如果需要监听IPv6
            if need_ipv6:
                need_blackbox = input("是否要添加Blackbox Explorer配置? (y/n): ").lower() == 'y'
                if need_blackbox:
                    ipv6_address = input("请输入IPv6地址 (例如: 2001:db8::1): ")
                    if not validate_ip(ipv6_address, allow_ipv6=True):
                        print("错误: 请输入有效的IPv6地址格式")
                        input("按Enter键继续...")
                        continue

            # 询问是否需要为blackbox_exporter配置basic auth
            print("提示: 建议为blackbox_exporter配置Basic认证以保护/metrics端点")
            need_basic_auth = input("是否需要为blackbox_exporter配置Basic认证? (y/n) [建议选y]: ").lower()
            basic_auth_username = None
            basic_auth_password = None
            if need_basic_auth == '' or need_basic_auth == 'y':
                basic_auth_username = input("请输入Basic认证用户名: ")
                basic_auth_password = input("请输入Basic认证密码: ")
                if not basic_auth_username or not basic_auth_password:
                    print("错误: 用户名和密码不能为空")
                    input("按Enter键继续...")
                    continue

            config = load_config()
            if add_target(config, target_ip, instance_name, code, city, filter_ipv6, ipv6_address, basic_auth_username, basic_auth_password):
                if save_config(config):
                    print(f"已成功添加IP为 {target_ip} 的目标。")
                    restart_prometheus()
                else:
                    print("添加目标到Prometheus配置失败。")
            else:
                print(f"目标 {target_ip} 已经存在，未进行任何更改。")

            input("按Enter键返回主菜单...")

        elif choice == '2':
            target_ip = input("请输入要删除的被控端IP地址 (例如: 192.168.1.1): ")
            if not validate_ip(target_ip):
                print("错误: 请输入有效的IP地址格式 (例如: 192.168.1.1)")
                input("按Enter键继续...")
                continue

            config = load_config()
            if remove_target(config, target_ip):
                if save_config(config):
                    print(f"已成功从Prometheus配置中删除IP为 {target_ip} 的目标。")
                    restart_prometheus()
                else:
                    print("删除目标失败，未能保存Prometheus配置文件。")
            else:
                print(f"未找到IP为 {target_ip} 的目标，配置未修改。")

            input("按Enter键返回主菜单...")

        elif choice == '3':
            print("退出程序。")
            break

        else:
            print("无效的选择，请重新输入。")
            input("按Enter键继续...")

if __name__ == "__main__":
    main()
