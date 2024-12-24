ENTITY_INFO_DICT = dict()


def get_entity_to_dict_info_by_obj_id(m_addr):
    """
    :desc 获取实体对象信息，优先从字典中读取，其次从数据库中读取
    :param m_addr：对象的内存地址
    :return: 设备详情对象
    """
    if m_addr in ENTITY_INFO_DICT:
        return ENTITY_INFO_DICT[m_addr]
    else:
        return None


def set_entity_to_dict_info_by_obj_id(m_addr, value: str):
    """
    :desc 设置实体对象信息，优先从字典中读取，其次从数据库中读取
    :param m_addr：对象的内存地址
    :param value：实体对象信息值
    :return: 设备详情对象
    """
    ENTITY_INFO_DICT[m_addr] = value
    return value
