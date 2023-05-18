

def state_sort(item):
    if item == "検討中":
        return 2
    elif item == "進行中":
        return 1        
    elif item == "テスト中":
        return 0        
    elif item == "完了":
        return 4        
    else:
        return 3
    
def value_sort(item):
    if item == "★★★":
        return 0
    elif item == "★★":
        return 1        
    elif item == "★":
        return 2        
    else:
        return 3

def progress_count(items):
    if not items:
        return
    complete_count = 0
    progression_count = 0
    idea_count = 0
    for item in items:
        item = item[0]
        if item == "進行中":
            progression_count += 1         
        elif item == "テスト中":
            idea_count += 1        
        elif item == "完了":
            complete_count += 1
        else:
            idea_count += 1
    ok = "0" * complete_count
    work = "o" * progression_count
    non_ok = "." * idea_count
    return ok + work + non_ok