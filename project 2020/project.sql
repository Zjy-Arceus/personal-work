SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- 数据库： `project fruit`
--

-- --------------------------------------------------------

--
-- 表的结构 `teacher`
--

CREATE TABLE `Teacher`( 
`Teacher_Name` VARCHAR(10) NOT NULL , 
`Password` INT(10) NOT NULL 
) ENGINE = InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `student`
--

CREATE TABLE `student` ( 
  `Stu_Name` VARCHAR(10) NOT NULL , 
  `Stu_ID` INT(10) NOT NULL , 
  `email` VARCHAR(30) NOT NULL , 
  `GPA` FLOAT(3) NULL DEFAULT NULL , 
  `Password` INT(10) NULL DEFAULT NULL , 
  `TeamNo` INT(2) NULL DEFAULT NULL , 
  `CourseID` INT(5) DEFAULT NULL
  ) ENGINE = InnoDB;

-- --------------------------------------------------------

--
-- 表的结构 `Team_All`
--

CREATE TABLE `Team_All` ( 
`CourseID` INT(5) NOT NULL,
`Stu_Name` VARCHAR(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
`TeamNO` INT(2) NOT NULL DEFAULT '1', 
`TeamName` VARCHAR(10) DEFAULT NULL
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `Course`
--

CREATE TABLE `course` ( 
`CourseID` INT(10) NOT NULL , 
`Course_Title` VARCHAR(10) NOT NULL , 
`Teacher_Name` VARCHAR(10) NOT NULL ,
 PRIMARY KEY (`CourseID`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `submission_item`
--

CREATE TABLE `submission_item` ( 
`Title` VARCHAR(10) NOT NULL , 
`Percentage` FLOAT(3) NOT NULL ,
`CourseID` INT(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `team_method`
--

CREATE TABLE `team_method` (
`CourseID` INT(5) NOT NULL,
`Total_Amount` INT(3) NOT NULL,
`Member_Num` INT(2) NOT NULL , 
`Free` BOOLEAN NOT NULL DEFAULT TRUE ,  
`Friend` BOOLEAN NOT NULL DEFAULT FALSE ,
`random` TINYINT(1) NOT NULL, 
`GPA_Consider` BOOLEAN NOT NULL DEFAULT FALSE,
`Multiple` VARCHAR(1) NULL DEFAULT NULL,
PRIMARY KEY (`CourseID`) 
) ENGINE = InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- 表的结构 `export_file`
--

CREATE TABLE `export_file` ( 
`Stu_Name` VARCHAR(10) NOT NULL , 
`Contribution` FLOAT(3) NOT NULL , 
`Bonus` INT(1) NOT NULL , 
`Identify` VARCHAR(1) NOT NULL , 
`CourseID` INT(10) NOT NULL , 
`TeamNO` INT(2) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `friend`
--

CREATE TABLE `friend` ( 
`Stu_Name` VARCHAR(10) NOT NULL , 
`Friend_Name` VARCHAR(10) NULL DEFAULT NULL , 
`Invitation_State` VARCHAR(15) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL, 
`Invitation_Name` VARCHAR(10) NULL DEFAULT NULL 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `team`
--

CREATE TABLE `team` ( 
`Stu_Name` VARCHAR(10) NOT NULL , 
`Contribution` FLOAT NULL DEFAULT '1' , 
`Bonus` FLOAT(3) NOT NULL DEFAULT '0', 
`Identify` VARCHAR(1) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT 'M', 
`CourseID` INT(10) NOT NULL , 
`TeamNO` INT(2) NOT NULL 
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `vote`
--

CREATE TABLE `vote` ( 
`TeamNO` INT(2) NOT NULL , 
`TeamName` VARCHAR(10) NOT NULL , 
`Stu_Name` VARCHAR(10) NOT NULL , 
`Votes` INT(2) NOT NULL,
`CheckVote` INT(1) NOT NULL DEFAULT '0' 
)ENGINE=InnoDB DEFAULT CHARSET=latin1;




CREATE TABLE `Temp_Ctr` ( 
  `CourseID` INT(5) NOT NULL , 
  `Stu_Name` VARCHAR(10) NOT NULL , 
  `Submission_Title` VARCHAR(10) NOT NULL , 
  `CheckSelect` INT(1) NOT NULL DEFAULT '0'
  ) ENGINE = InnoDB;




CREATE TABLE `TableSum` ( 
  `CourseID` INT(5) NOT NULL, 
  `Num` INT(2) NOT NULL DEFAULT '0', 
  PRIMARY KEY (`CourseID`)
  ) ENGINE = InnoDB;



INSERT INTO `course` (`CourseID`, `Course_Title`, `Teacher_Name`) VALUES ('1001', 'Math', 'Wang'), ('1002', 'Chinese', 'Wang_Chn'), ('1003', 'java', 'Jack_java');

INSERT INTO `teacher` (`Teacher_Name`, `Password`) VALUES ('Wang', '123'), ('Wang_Chn', '123'), ('Jack_java', '123')


-- --------------------------------------------------------

