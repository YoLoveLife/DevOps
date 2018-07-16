-- MySQL dump 10.16  Distrib 10.1.12-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: deveops_dev
-- ------------------------------------------------------
-- Server version	10.1.12-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (4,'DBA'),(6,'安全工程师'),(5,'开发工程师'),(2,'资产配置管理员'),(3,'运维工程师');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (148,2,12),(5,2,17),(6,2,18),(7,2,19),(8,2,20),(9,2,21),(10,2,25),(11,2,26),(12,2,27),(13,2,28),(14,2,32),(15,2,33),(16,2,34),(17,2,35),(18,2,36),(19,2,37),(20,2,38),(21,2,39),(22,2,40),(23,2,41),(116,2,48),(144,2,49),(145,2,50),(146,2,51),(147,2,52),(24,2,56),(25,2,57),(102,2,58),(26,2,59),(27,2,60),(28,2,61),(117,2,65),(137,2,66),(138,2,67),(139,2,68),(140,2,69),(29,2,73),(141,2,74),(142,2,75),(143,2,76),(32,2,77),(133,3,4),(132,3,5),(135,3,6),(136,3,7),(150,3,12),(123,3,17),(122,3,20),(121,3,25),(118,3,32),(119,3,33),(41,3,48),(110,3,49),(111,3,50),(112,3,51),(113,3,52),(114,3,56),(115,3,59),(44,3,65),(103,3,66),(104,3,67),(105,3,68),(106,3,69),(107,3,73),(149,3,74),(108,3,75),(151,3,78),(109,3,79),(45,3,83),(46,3,84),(47,3,85),(48,3,86),(49,3,90),(50,3,91),(51,3,92),(52,3,93),(53,3,103),(54,3,104),(55,3,105),(56,3,106),(57,3,110),(126,3,111),(58,3,112),(59,3,113),(124,3,114),(125,3,115),(60,3,117),(61,3,127),(33,3,128),(34,3,129),(35,3,139),(36,3,146),(37,3,147),(38,3,148),(39,3,149),(40,3,150),(42,3,178),(43,3,179),(71,4,154),(72,4,155),(73,4,156),(74,4,157),(75,4,158),(76,4,159),(62,4,163),(63,4,164),(64,4,165),(65,4,166),(66,4,170),(67,4,171),(68,4,172),(69,4,173),(70,4,174),(77,5,4),(78,5,5),(134,5,6),(79,5,7),(87,5,48),(89,5,51),(91,5,56),(92,5,59),(93,5,65),(94,5,68),(95,5,73),(96,5,103),(97,5,110),(98,5,111),(99,5,112),(100,5,114),(101,5,115),(80,5,146),(81,5,149),(82,5,154),(83,5,158),(84,5,163),(85,5,170),(86,5,174),(88,5,178),(90,5,179),(127,5,210),(128,5,211),(120,6,73),(129,6,210),(130,6,212),(131,6,213);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=214 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add file',1,'add_file'),(2,'Can change file',1,'change_file'),(3,'Can delete file',1,'delete_file'),(4,'罗列文件',1,'yo_list_file'),(5,'上传文件',1,'yo_create_file'),(6,'修改文件',1,'yo_update_file'),(7,'删除文件',1,'yo_delete_file'),(8,'Can add image',2,'add_image'),(9,'Can change image',2,'change_image'),(10,'Can delete image',2,'delete_image'),(11,'罗列图片',2,'yo_list_image'),(12,'上传图片',2,'yo_create_image'),(13,'删除图片',2,'yo_delete_image'),(14,'Can add jumper',3,'add_jumper'),(15,'Can change jumper',3,'change_jumper'),(16,'Can delete jumper',3,'delete_jumper'),(17,'罗列跳板机',3,'yo_list_jumper'),(18,'创建跳板机',3,'yo_create_jumper'),(19,'更新跳板机',3,'yo_update_jumper'),(20,'刷新跳板机器',3,'yo_status_jumper'),(21,'删除跳板机',3,'yo_delete_jumper'),(22,'Can add key',4,'add_key'),(23,'Can change key',4,'change_key'),(24,'Can delete key',4,'delete_key'),(25,'罗列密钥',4,'yo_list_key'),(26,'创建密钥',4,'yo_create_key'),(27,'更新密钥',4,'yo_update_key'),(28,'删除密钥',4,'yo_delete_key'),(29,'Can add extend user',5,'add_extenduser'),(30,'Can change extend user',5,'change_extenduser'),(31,'Can delete extend user',5,'delete_extenduser'),(32,'罗列用户',5,'yo_list_user'),(33,'罗列运维用户',5,'yo_list_opsuser'),(34,'新增用户',5,'yo_create_user'),(35,'修改用户',5,'yo_update_user'),(36,'删除用户',5,'yo_delete_user'),(37,'罗列权限组',5,'yo_list_pmngroup'),(38,'新增权限组',5,'yo_create_pmngroup'),(39,'修改权限组',5,'yo_update_pmngroup'),(40,'删除权限组',5,'yo_delete_pmngroup'),(41,'罗列所有权限',5,'yo_list_permission'),(42,'Can add host detail',6,'add_hostdetail'),(43,'Can change host detail',6,'change_hostdetail'),(44,'Can delete host detail',6,'delete_hostdetail'),(45,'Can add system_ type',7,'add_system_type'),(46,'Can change system_ type',7,'change_system_type'),(47,'Can delete system_ type',7,'delete_system_type'),(48,'罗列系统类型',7,'yo_list_systype'),(49,'新增系统类型',7,'yo_create_systype'),(50,'修改系统类型',7,'yo_update_systype'),(51,'详细系统类型',7,'yo_detail_systype'),(52,'删除系统类型',7,'yo_delete_systype'),(53,'Can add group',8,'add_group'),(54,'Can change group',8,'change_group'),(55,'Can delete group',8,'delete_group'),(56,'罗列应用组',8,'yo_list_group'),(57,'新增应用组',8,'yo_create_group'),(58,'修改应用组',8,'yo_update_group'),(59,'详细查看应用组',8,'yo_detail_group'),(60,'删除应用组',8,'yo_delete_group'),(61,'批量归类主机',8,'yo_group_sort_host'),(62,'Can add position',9,'add_position'),(63,'Can change position',9,'change_position'),(64,'Can delete position',9,'delete_position'),(65,'罗列位置',9,'yo_list_position'),(66,'新增位置',9,'yo_create_position'),(67,'修改位置',9,'yo_update_position'),(68,'详细位置',9,'yo_detail_position'),(69,'删除位置',9,'yo_delete_position'),(70,'Can add host',10,'add_host'),(71,'Can change host',10,'change_host'),(72,'Can delete host',10,'delete_host'),(73,'罗列主机',10,'yo_list_host'),(74,'新增主机',10,'yo_create_host'),(75,'修改主机',10,'yo_update_host'),(76,'删除主机',10,'yo_delete_host'),(77,'更改主机应用组',10,'yo_host_sort_group'),(78,'获取主机密码',10,'yo_passwd_host'),(79,'远控主机',10,'yo_webskt_host'),(80,'Can add meta',11,'add_meta'),(81,'Can change meta',11,'change_meta'),(82,'Can delete meta',11,'delete_meta'),(83,'罗列元操作',11,'yo_list_meta'),(84,'创建元操作',11,'yo_create_meta'),(85,'更新元操作',11,'yo_update_meta'),(86,'删除元操作',11,'yo_delete_meta'),(87,'Can add met a_content',12,'add_meta_content'),(88,'Can change met a_content',12,'change_meta_content'),(89,'Can delete met a_content',12,'delete_meta_content'),(90,'罗列元操作内容',12,'yo_list_metacontent'),(91,'创建元操作内容',12,'yo_create_metacontent'),(92,'更新元操作内容',12,'yo_update_metacontent'),(93,'删除元操作内容',12,'yo_delete_metacontent'),(94,'Can add met a_sort',13,'add_meta_sort'),(95,'Can change met a_sort',13,'change_meta_sort'),(96,'Can delete met a_sort',13,'delete_meta_sort'),(97,'Can add push_ mission',14,'add_push_mission'),(98,'Can change push_ mission',14,'change_push_mission'),(99,'Can delete push_ mission',14,'delete_push_mission'),(100,'Can add mission',15,'add_mission'),(101,'Can change mission',15,'change_mission'),(102,'Can delete mission',15,'delete_mission'),(103,'罗列任务',15,'yo_list_mission'),(104,'创建任务',15,'yo_create_mission'),(105,'更新任务',15,'yo_update_mission'),(106,'删除任务',15,'yo_delete_mission'),(107,'Can add code_ work',16,'add_code_work'),(108,'Can change code_ work',16,'change_code_work'),(109,'Can delete code_ work',16,'delete_code_work'),(110,'罗列发布工单',16,'yo_list_codework'),(111,'新增发布工单',16,'yo_create_codework'),(112,'详细查看发布工单',16,'yo_detail_codework'),(113,'审核发布工单',16,'yo_exam_codework'),(114,'运行发布工单',16,'yo_run_codework'),(115,'为工单上传文件',16,'yo_upload_codework'),(116,'删除应用组',16,'yo_delete_codework'),(117,'查看错误工单信息',16,'yo_results_codework'),(118,'Can add safety_ work',17,'add_safety_work'),(119,'Can change safety_ work',17,'change_safety_work'),(120,'Can delete safety_ work',17,'delete_safety_work'),(121,'Can add history',18,'add_history'),(122,'Can change history',18,'change_history'),(123,'Can delete history',18,'delete_history'),(124,'Can add var2 group',19,'add_var2group'),(125,'Can change var2 group',19,'change_var2group'),(126,'Can delete var2 group',19,'delete_var2group'),(127,'罗列组参数',19,'yo_list_group_var'),(128,'新增组参数',19,'yo_change_group_var'),(129,'删除组参数',19,'yo_delete_group_var'),(130,'Can add expired aliyun mongo db',20,'add_expiredaliyunmongodb'),(131,'Can change expired aliyun mongo db',20,'change_expiredaliyunmongodb'),(132,'Can delete expired aliyun mongo db',20,'delete_expiredaliyunmongodb'),(133,'Can add expired aliyun rds',21,'add_expiredaliyunrds'),(134,'Can change expired aliyun rds',21,'change_expiredaliyunrds'),(135,'Can delete expired aliyun rds',21,'delete_expiredaliyunrds'),(136,'Can add expired aliyun ecs',22,'add_expiredaliyunecs'),(137,'Can change expired aliyun ecs',22,'change_expiredaliyunecs'),(138,'Can delete expired aliyun ecs',22,'delete_expiredaliyunecs'),(139,'罗列过期资源',22,'yo_list_expired'),(140,'Can add expired aliyun kv store',23,'add_expiredaliyunkvstore'),(141,'Can change expired aliyun kv store',23,'change_expiredaliyunkvstore'),(142,'Can delete expired aliyun kv store',23,'delete_expiredaliyunkvstore'),(143,'Can add dns',24,'add_dns'),(144,'Can change dns',24,'change_dns'),(145,'Can delete dns',24,'delete_dns'),(146,'罗列域名',24,'yo_list_dns'),(147,'新增域名',24,'yo_create_dns'),(148,'修改域名',24,'yo_update_dns'),(149,'详细查看域名',24,'yo_detail_dns'),(150,'删除域名',24,'yo_delete_dns'),(151,'Can add instance',25,'add_instance'),(152,'Can change instance',25,'change_instance'),(153,'Can delete instance',25,'delete_instance'),(154,'罗列数据库实例',25,'yo_list_db'),(155,'新增数据库实例',25,'yo_create_db'),(156,'修改数据库实例',25,'yo_update_db'),(157,'删除数据库实例',25,'yo_delete_db'),(158,'详细查看数据库实例',25,'yo_detail_db'),(159,'获取数据库实例密码',25,'yo_passwd_db'),(160,'Can add role',26,'add_role'),(161,'Can change role',26,'change_role'),(162,'Can delete role',26,'delete_role'),(163,'罗列数据库角色',26,'yo_list_db_role'),(164,'新增数据库角色',26,'yo_create_db_role'),(165,'修改数据库角色',26,'yo_update_db_role'),(166,'删除数据库角色',26,'yo_delete_db_role'),(167,'Can add user',27,'add_user'),(168,'Can change user',27,'change_user'),(169,'Can delete user',27,'delete_user'),(170,'罗列数据库用户',27,'yo_list_db_user'),(171,'新增数据库用户',27,'yo_create_db_user'),(172,'修改数据库用户',27,'yo_update_db_user'),(173,'删除数据库用户',27,'yo_delete_db_user'),(174,'获取数据库实例用户',27,'yo_passwd_db_user'),(175,'Can add monitor',28,'add_monitor'),(176,'Can change monitor',28,'change_monitor'),(177,'Can delete monitor',28,'delete_monitor'),(178,'阿里云监控查看',28,'yo_monitor_aliyun'),(179,'VMware监控查看',28,'yo_monitor_vmware'),(180,'Can add permission',29,'add_permission'),(181,'Can change permission',29,'change_permission'),(182,'Can delete permission',29,'delete_permission'),(183,'Can add group',30,'add_group'),(184,'Can change group',30,'change_group'),(185,'Can delete group',30,'delete_group'),(186,'Can add content type',31,'add_contenttype'),(187,'Can change content type',31,'change_contenttype'),(188,'Can delete content type',31,'delete_contenttype'),(189,'Can add session',32,'add_session'),(190,'Can change session',32,'change_session'),(191,'Can delete session',32,'delete_session'),(192,'Can add periodic task',33,'add_periodictask'),(193,'Can change periodic task',33,'change_periodictask'),(194,'Can delete periodic task',33,'delete_periodictask'),(195,'Can add crontab',34,'add_crontabschedule'),(196,'Can change crontab',34,'change_crontabschedule'),(197,'Can delete crontab',34,'delete_crontabschedule'),(198,'Can add interval',35,'add_intervalschedule'),(199,'Can change interval',35,'change_intervalschedule'),(200,'Can delete interval',35,'delete_intervalschedule'),(201,'Can add solar event',36,'add_solarschedule'),(202,'Can change solar event',36,'change_solarschedule'),(203,'Can delete solar event',36,'delete_solarschedule'),(204,'Can add periodic tasks',37,'add_periodictasks'),(205,'Can change periodic tasks',37,'change_periodictasks'),(206,'Can delete periodic tasks',37,'delete_periodictasks'),(207,'Can add safe_ work',38,'add_safe_work'),(208,'Can change safe_ work',38,'change_safe_work'),(209,'Can delete safe_ work',38,'delete_safe_work'),(210,'罗列安全工单',38,'yo_list_safework'),(211,'新增安全工单',38,'yo_create_safework'),(212,'修改安全工单状态',38,'yo_status_safework'),(213,'详细查看安全工单',38,'yo_detail_safework');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authority_extenduser_groups`
--

DROP TABLE IF EXISTS `authority_extenduser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authority_extenduser_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `extenduser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `authority_extenduser_groups_extenduser_id_group_id_6b5d2ab6_uniq` (`extenduser_id`,`group_id`),
  KEY `authority_extenduser_groups_group_id_2a9a801f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `authority_extenduser_extenduser_id_b9dacd96_fk_authority` FOREIGN KEY (`extenduser_id`) REFERENCES `authority_extenduser` (`id`),
  CONSTRAINT `authority_extenduser_groups_group_id_2a9a801f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authority_extenduser_groups`
--

LOCK TABLES `authority_extenduser_groups` WRITE;
/*!40000 ALTER TABLE `authority_extenduser_groups` DISABLE KEYS */;
INSERT INTO `authority_extenduser_groups` VALUES (2,2,3),(3,3,5),(4,4,2),(5,5,4),(6,6,4);
/*!40000 ALTER TABLE `authority_extenduser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (30,'auth','group'),(29,'auth','permission'),(5,'authority','extenduser'),(3,'authority','jumper'),(4,'authority','key'),(31,'contenttypes','contenttype'),(22,'dashboard','expiredaliyunecs'),(23,'dashboard','expiredaliyunkvstore'),(20,'dashboard','expiredaliyunmongodb'),(21,'dashboard','expiredaliyunrds'),(25,'db','instance'),(26,'db','role'),(27,'db','user'),(34,'django_celery_beat','crontabschedule'),(35,'django_celery_beat','intervalschedule'),(33,'django_celery_beat','periodictask'),(37,'django_celery_beat','periodictasks'),(36,'django_celery_beat','solarschedule'),(8,'manager','group'),(10,'manager','host'),(6,'manager','hostdetail'),(9,'manager','position'),(7,'manager','system_type'),(28,'monitor','monitor'),(11,'ops','meta'),(12,'ops','meta_content'),(13,'ops','meta_sort'),(15,'ops','mission'),(14,'ops','push_mission'),(32,'sessions','session'),(18,'timeline','history'),(1,'utils','file'),(2,'utils','image'),(19,'variable','var2group'),(16,'work','code_work'),(17,'work','safety_work'),(38,'work','safe_work'),(24,'yodns','dns');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-15 16:32:47
