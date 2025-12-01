import os
from selenium import webdriver
from .settings import KEY_MAP

def create_directory_structure():
    """创建完整的目录结构"""
    
    # 创建根目录（如果需要）
    root_dir = "农业分类目录"
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
        print(f"创建根目录: {root_dir}")
    
    created_count = 0
    
    # 遍历第一级目录
    for level1, level2_dict in KEY_MAP.items():
        level1_path = os.path.join(root_dir, level1)
        
        # 检查并创建第一级目录
        if not os.path.exists(level1_path):
            os.makedirs(level1_path)
            print(f"创建第一级目录: {level1}")
            created_count += 1
        
        # 遍历第二级目录
        for level2, level3_list in level2_dict.items():
            level2_path = os.path.join(level1_path, level2)
            
            # 检查并创建第二级目录
            if not os.path.exists(level2_path):
                os.makedirs(level2_path)
                print(f"  创建第二级目录: {level2}")
                created_count += 1
            
            # 遍历第三级目录
            for level3 in level3_list:
                level3_path = os.path.join(level2_path, level3)
                
                # 检查并创建第三级目录
                if not os.path.exists(level3_path):
                    os.makedirs(level3_path)
                    print(f"    创建第三级目录: {level3}")
                    created_count += 1
                
                # 在第三级目录下创建"附件"文件夹
                attachment_path = os.path.join(level3_path, "附件")
                if not os.path.exists(attachment_path):
                    os.makedirs(attachment_path)
                    print(f"      创建附件目录: {level3}/附件")
                    created_count += 1
    
    return created_count

def check_existing_structure():
    """检查现有目录结构"""
    
    root_dir = "农业分类目录"
    if not os.path.exists(root_dir):
        print("根目录不存在")
        return 0
    
    existing_count = 0
    missing_dirs = []
    
    for level1, level2_dict in KEY_MAP.items():
        level1_path = os.path.join(root_dir, level1)
        
        if not os.path.exists(level1_path):
            missing_dirs.append(f"第一级目录: {level1}")
            continue
        
        for level2, level3_list in level2_dict.items():
            level2_path = os.path.join(level1_path, level2)
            
            if not os.path.exists(level2_path):
                missing_dirs.append(f"第二级目录: {level1}/{level2}")
                continue
            
            for level3 in level3_list:
                level3_path = os.path.join(level2_path, level3)
                attachment_path = os.path.join(level3_path, "附件")
                
                if not os.path.exists(level3_path):
                    missing_dirs.append(f"第三级目录: {level1}/{level2}/{level3}")
                elif not os.path.exists(attachment_path):
                    missing_dirs.append(f"附件目录: {level1}/{level2}/{level3}/附件")
                else:
                    existing_count += 1
    
    if missing_dirs:
        print("\n缺失的目录:")
        for dir_path in missing_dirs:
            print(f"  - {dir_path}")
    
    return existing_count

def MakeDir():
    """主函数"""
    # print("农业分类目录生成器")
    # print("=" * 50)
    print("[log]: 检查目录结构")
    # 检查现有结构
    existing_count = check_existing_structure()

    if existing_count < 63:
        print("[log]: 目录结构不完整，开始创建目录")
        create_directory_structure()
        print("[log]: 目录创建成功")
    
    print("[log]: 目录结构完整")
    
    # if existing_count > 0:
    #     print(f"\n已存在的完整目录数量: {existing_count}")
    #     choice = input("\n是否继续创建缺失的目录? (y/n): ").lower()
    #     if choice != 'y':
    #         #print("操作已取消")
    #         return
    
    # print("\n开始创建目录结构...")
    # created_count = create_directory_structure()
    
    # print(f"\n操作完成! 共创建了 {created_count} 个目录")
    
    # 显示最终目录统计
    # total_dirs = sum(len(level3_list) for level2_dict in KEY_MAP.values() for level3_list in level2_dict.values())
    # total_with_attachments = total_dirs * 2  # 每个三级目录都对应一个附件目录
    
    # print(f"\n目录统计:")
    # print(f"第一级目录: {len(KEY_MAP)} 个")
    # second_level_count = sum(len(level2_dict) for level2_dict in KEY_MAP.values())
    # print(f"第二级目录: {second_level_count} 个")
    # print(f"第三级目录: {total_dirs} 个")
    # print(f"附件目录: {total_dirs} 个")
    # print(f"总计: {len(KEY_MAP) + second_level_count + total_with_attachments} 个目录")

def MakeDriver():
    # 打开浏览器
    print("[WebDriver]: 初始化浏览器")
    options = webdriver.FirefoxOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(30)
    print("[WebDdriver]: 初始化浏览器成功")
    return driver

MakeDir()
driver = MakeDriver()