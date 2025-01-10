
CREATE TABLE entity_weight_info(

);


CREATE TABLE entity_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    flags JSON,
    value JSON,
    label_name VARCHAR(255),
    version VARCHAR(255),
    cmd_flag_list JSON,
    cmd_operand_list JSON,
    method VARCHAR(255),
    url VARCHAR(255),
    cmd_list JSON,
    cmd_type VARCHAR(255),
    pkg_list JSON,
    version_list JSON,
    src VARCHAR(255),
    dest VARCHAR(255),
    types VARCHAR(255)
);
