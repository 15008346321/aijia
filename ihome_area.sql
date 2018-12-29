/*
Navicat MySQL Data Transfer

Source Server         : 本地服务器
Source Server Version : 50557
Source Host           : localhost:3306
Source Database       : aj

Target Server Type    : MYSQL
Target Server Version : 50557
File Encoding         : 65001

Date: 2018-06-20 16:19:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ihome_area
-- ----------------------------
DROP TABLE IF EXISTS `ihome_area`;
CREATE TABLE `ihome_area` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ihome_area
-- ----------------------------
INSERT INTO `ihome_area` VALUES (null, null, '1', '锦江区');
INSERT INTO `ihome_area` VALUES (null, null, '2', '金牛区');
INSERT INTO `ihome_area` VALUES (null, null, '3', '青羊区');
INSERT INTO `ihome_area` VALUES (null, null, '4', '高新区');
INSERT INTO `ihome_area` VALUES (null, null, '5', '武侯区');
INSERT INTO `ihome_area` VALUES (null, null, '6', '天府新区');
INSERT INTO `ihome_area` VALUES (null, null, '7', '双流县');
INSERT INTO `ihome_area` VALUES (null, null, '8', '成华区');
INSERT INTO `ihome_area` VALUES (null, null, '9', '青白江区');
INSERT INTO `ihome_area` VALUES (null, null, '10', '新都区');
INSERT INTO `ihome_area` VALUES (null, null, '11', '温江区');
INSERT INTO `ihome_area` VALUES (null, null, '12', '郫县');
INSERT INTO `ihome_area` VALUES (null, null, '13', '蒲江县');
INSERT INTO `ihome_area` VALUES (null, null, '14', '大邑县');
INSERT INTO `ihome_area` VALUES (null, null, '15', '新津县');

-- ----------------------------
-- Table structure for ihome_facility
-- ----------------------------
DROP TABLE IF EXISTS `ihome_facility`;
CREATE TABLE `ihome_facility` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `css` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ihome_facility
-- ----------------------------
INSERT INTO `ihome_facility` VALUES (null, null, '1', '无线网络', 'wirelessnetwork-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '2', '热水淋浴', 'shower-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '3', '空调', 'aircondition-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '4', '暖气', 'heater-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '5', '允许吸烟', 'smoke-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '6', '饮水设备', 'drinking-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '7', '牙具', 'brush-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '8', '香皂', 'soap-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '9', '拖鞋', 'slippers-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '10', '手纸', 'toiletpaper-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '11', '毛巾', 'towel-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '12', '沐浴露、洗发露', 'toiletries-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '13', '冰箱', 'icebox-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '14', '洗衣机', 'washer-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '15', '电梯', 'elevator-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '16', '允许做饭', 'iscook-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '17', '允许带宠物', 'pet-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '18', '允许聚会', 'meet-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '19', '门禁系统', 'accesssys-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '20', '停车位', 'parkingspace-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '21', '有线网络', 'wirednetwork-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '22', '电视', 'tv-ico');
INSERT INTO `ihome_facility` VALUES (null, null, '23', '浴缸', 'jinzhi-ico');
