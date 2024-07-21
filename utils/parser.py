from pathlib import Path
from lxml import etree
import json

from log import Logger


class JobDetailParser:
    def __int__(self, html: str):
        self.html_str = html
        self.lxml_obj = etree.HTML(html)

        # 保存日志的目录
        self.log_dir = Path('./log')
        self.log_dir.mkdir(exist_ok=True)

        # 日志, 保存时以时间命名
        self.logger = Logger(self.log_dir / 'job_detail_parser.log')

        # xpath 规则
        self.xpath = {
            # ---------------- 招聘简介 ----------------
            # 岗位名
            'title': '//div[@id="main"]//div[@class="info-primary"]//div[@class="name"]/h1/text()',

            # 薪资
            'salary': '//div[@id="main"]//div[@class="info-primary"]//div[@class="name"]/span/text()',

            # 所在市
            'city': '//div[@id="main"]//div[@class="info-primary"]//p/a/text()',

            # 工作经验 (在校/应届)
            'experience': '//div[@id="main"]//div[@class="info-primary"]//p/span[1]/text()',

            # 学历要求
            'education': '//div[@id="main"]//div[@class="info-primary"]//p/span[2]/text()',

            # 职位描述
            'description': '//div[@id="main"]//div[@class="job-detail-section"]/ul[@class="job-keyword-list"]/li/text()',

            # 若是应届生, 则有这个字段
            'graduation': 'string(//div[@id="main"]//div[@class="job-detail-section"]/p[@class="school-job-sec"])',

            # 职位要求
            'requirement': '//div[@id="main"]//div[@class="job-detail-section"]/div[@class="job-sec-text"]/text()',

            # ---------------- 公司简介 ----------------
            # 公司名称
            'company': '//div[@id="main"]//div[@class="sider-company"]/div[@class="company-info"]/a[2]/text',

            # 公司 logo
            'logo_url': '//div[@id="main"]//div[@class="sider-company"]/div[@class="company-info"]/a[1]/img/@src',

            # 是否要融资
            'financing': '//div[@id="main"]//div[@class="sider-company"]/p[2]/text()',

            # 公司规模
            'company_size': '//div[@id="main"]//div[@class="sider-company"]/p[3]/text()',

            # 行业
            'industry': '//div[@id="main"]//div[@class="sider-company"]/p[4]/a/text()',

            # ---------------- 工商信息 ----------------
            # 公司名称
            'business_info_company-name': '//div[@id="main"]//div[@class="level-list-box"]/ul/li[1]/text()',

            # 法定代表人
            'business_info_company-user': '//div[@id="main"]//div[@class="level-list-box"]/ul/li[2]/text()',

            # 成立时间
            'business_info_company-res-time': '//div[@id="main"]//div[@class="level-list-box"]/ul/li[3]/text()',

            # 公司类型
            'business_info_company-conpany-type': '//div[@id="main"]//div[@class="level-list-box"]/ul/li[4]/text()',

            # 经营状态
            'business_info_company-manage-state': '//div[@id="main"]//div[@class="level-list-box"]/ul/li[5]/text()',

            # 注册资金
            'business_info_company-company-fund': '//div[@id="main"]//div[@class="level-list-box"]/ul/li[6]/text()',

            # 地点
            'location': '',
        }

    def safe_extract(self, xpath, desc: str):
        try:
            result = self.lxml_obj.xpath(xpath)
            return result
        except Exception as e:
            self.logger.error(f'{desc}: 解析错误')
            return ''

    def parse(self):
        # 招聘简介
        # 岗位名称
        title = self.safe_extract(self.xpath['title'], '岗位名')

        # 薪资
        salary = self.safe_extract(self.xpath['salary'], '薪资')

        # 所在市
        city = self.safe_extract(self.xpath['city'], '所在市')

        # 工作经验 (在校/应届)
        experience = self.safe_extract(self.xpath['experience'], '工作经验')

        # 学历要求
        education = self.safe_extract(self.xpath['education'], '学历要求')

        # 职位描述
        description = self.safe_extract(self.xpath['description'], '职位描述')

        # 若是应届生, 则有这个字段
        graduation = self.safe_extract(self.xpath['graduation'], '毕业生')

        # 职位要求
        requirement = self.safe_extract(self.xpath['requirement'], '职位要求')

        # 公司简介
        # 公司名称
        company = self.safe_extract(self.xpath['company'], '公司名')

        # 公司 logo
        logo_url = self.safe_extract(self.xpath['logo'], '公司 logo')

        # 是否要融资
        financing = self.safe_extract(self.xpath['financing'], '是否要融资')

        # 公司规模
        company_size = self.safe_extract(self.xpath['company_size'], '公司人数')

        # 所属行业
        industry = self.safe_extract(self.xpath['industry'], '行业')

        # 工商信息
        # 公司名称
        business_info_company_name = self.safe_extract(self.xpath['business_info_company-name'], '公司名称')

        # 法定代表人
        business_info_company_user = self.safe_extract(self.xpath['business_info_company-user'], '法定代表人')

        # 成立时间
        business_info_company_res_time = self.safe_extract(self.xpath['business_info_company-res-time'], '成立时间')

        # 公司类型
        business_info_company_conpany_type = self.safe_extract(self.xpath['business_info_company-conpany-type'],
                                                               '公司类型')

        # 经营状态
        business_info_company_manage_state = self.safe_extract(self.xpath['business_info_company-manage-state'],
                                                               '经营状态')

        # 注册资金
        business_info_company_company_fund = self.safe_extract(self.xpath['business_info_company-company-fund'],
                                                               '注册资金')

        # 地点
        location = self.safe_extract(self.xpath['location'], '地点')


class JobListJsonParser:
    def __int__(self):
        self.json: json = None
        self.count = 0

    def parse(self, json_):
        self.json = json_

        if not self.json:
            return []
        if not isinstance(self.json, dict):
            return []

        if self.json.get('code') is None or self.json.get('message') is None:
            return []

        if self.json['code'] != '0' or self.json['message'] != 'Success':
            return []

        if self.json.get('zpData') is None or self.json['zpData'].get('jobList') is None:
            return []

        for job in self.json['zpData']['jobList']:
            securityId = job.get('securityId')
            bossAvatar = job.get('bossAvatar')  # hr 的头像
            bossCert = job.get('bossCert')  # hr 的信用
            encryptBossId = job.get('encryptBossId')
            bossName = job.get('bossName')  # hr 的名字
            goldHunter = job.get('goldHunter')  # 是否是金牌猎头
            bossOnline = job.get('bossOnline')  # hr 是否在线
            encryptJobId = job.get('encryptJobId')
            expectId = job.get('expectId')

            jobName = job.get('jobName')  # 岗位名称
            lid = job.get('lid')
            salaryDesc = job.get('salaryDesc')  # 薪资
            jobLabels: list = job.get('jobLabels')  # 工作经验 (在校/应届)
            jobValidStatus = job.get('jobValidStatus')
            skills: list = job.get('skills')  # 技能要求
            jobExperience = job.get('jobExperience')  # 工作经验 (在校/应届)
            daysPerWeekDesc = job.get('daysPerWeekDesc')
            leastMonthDesc = job.get('leastMonthDesc')
            jobDegree = job.get('jobDegree')  # 学历要求

            cityName = job.get('cityName')  # 所在市
            areaDistrict = job.get('areaDistrict')  # 区
            businessDistrict = job.get('businessDistrict')  # 商圈

            jobType = job.get('jobType')
            proxyJob = job.get('proxyJob')
            proxyType = job.get('proxyType')
            anonymous = job.get('anonymous')
            outland = job.get('outland')
            optimal = job.get('optimal')
            isShield = job.get('isShield')
            atsDirectPost = job.get('atsDirectPost')
            gps = job.get('gps')

            encryptBrandId = job.get('encryptBrandId')
            brandName = job.get('brandName')  # 品牌名 公司名称
            brandLogo = job.get('brandLogo')  # 公司 logo
            brandStageName = job.get('brandStageName')  # 融资
            brandIndustry = job.get('brandIndustry')  # 行业
            brandScaleName = job.get('brandScaleName')  # 公司人数
            welfareList: list = job.get('welfareList')  # 福利

