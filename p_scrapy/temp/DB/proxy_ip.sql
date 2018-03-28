/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50703
Source Host           : localhost:3306
Source Database       : jiayuan

Target Server Type    : MYSQL
Target Server Version : 50703
File Encoding         : 65001

Date: 2018-03-28 23:55:32
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `proxy_ip`
-- ----------------------------
DROP TABLE IF EXISTS `proxy_ip`;
CREATE TABLE `proxy_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_port` varchar(50) NOT NULL COMMENT '代理IP',
  `port` int(10) DEFAULT NULL COMMENT '端口，暂时保留',
  `is_current` varchar(6) NOT NULL DEFAULT '0' COMMENT '是否是当前使用的IP，1为当前使用IP',
  `validate` int(6) NOT NULL DEFAULT '1' COMMENT '是否验证有效，1有效0无效',
  `priority` int(11) DEFAULT '0' COMMENT 'IP使用优先级，数字越低，优先级越高',
  `last_time_use` datetime DEFAULT NULL COMMENT '该IP上次访问时间',
  `use_times` varchar(10) DEFAULT NULL COMMENT '该IP使用时间单位为秒',
  `user_agent` varchar(500) DEFAULT NULL COMMENT '代理的user_agent',
  PRIMARY KEY (`id`,`ip_port`)
) ENGINE=InnoDB AUTO_INCREMENT=821 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of proxy_ip
-- ----------------------------
INSERT INTO `proxy_ip` VALUES ('805', '122.114.31.177:808', null, '0', '1', '0', null, null, 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6');
INSERT INTO `proxy_ip` VALUES ('806', '61.135.217.7:80', null, '0', '1', '0', '2018-03-28 22:59:10', '3', 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3');
INSERT INTO `proxy_ip` VALUES ('807', '118.212.137.135:31288', null, '0', '1', '0', '2018-03-28 23:01:31', '6', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3');
INSERT INTO `proxy_ip` VALUES ('808', '211.159.177.212:3128', null, '0', '1', '0', '2018-03-28 23:01:46', '0', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3');
INSERT INTO `proxy_ip` VALUES ('809', '121.31.102.44:8123', null, '0', '1', '0', '2018-03-28 23:11:42', '0', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3');
INSERT INTO `proxy_ip` VALUES ('810', '124.193.37.5:8888', null, '0', '1', '0', '2018-03-28 22:58:54', '0', 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11');
INSERT INTO `proxy_ip` VALUES ('811', '119.28.138.104:3128', null, '0', '1', '0', '2018-03-28 22:58:56', '3', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24');
INSERT INTO `proxy_ip` VALUES ('812', '111.155.124.77:8123', null, '0', '1', '0', '2018-03-28 23:05:56', '6', 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3');
INSERT INTO `proxy_ip` VALUES ('813', '203.174.112.13:3128', null, '0', '1', '0', '2018-03-28 22:59:30', '8', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3');
INSERT INTO `proxy_ip` VALUES ('814', '110.73.47.207:8123', null, '1', '1', '0', '2018-03-28 23:55:28', '4', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24');
INSERT INTO `proxy_ip` VALUES ('815', '124.128.39.138:8080', null, '0', '1', '0', '2018-03-28 22:47:17', '4', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3');
INSERT INTO `proxy_ip` VALUES ('816', '175.6.2.174:8088', null, '0', '1', '0', '2018-03-28 22:49:31', '6', 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3');
INSERT INTO `proxy_ip` VALUES ('817', '223.145.229.63:6666', null, '0', '1', '0', '2018-03-28 22:50:26', '8', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5');
INSERT INTO `proxy_ip` VALUES ('818', '111.8.191.150:8908', null, '0', '1', '0', '2018-03-28 22:58:17', '3', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3');
INSERT INTO `proxy_ip` VALUES ('819', '159.255.163.189:80', null, '0', '1', '0', null, null, 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1');
INSERT INTO `proxy_ip` VALUES ('820', '223.146.105.30:808', null, '0', '1', '0', null, null, 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3');
