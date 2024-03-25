class User{
    constructor(userId, userName, displayName){
        this.userId = userId;
        this.userName = userName;
        this.displayName = displayName;
    }
}

class Makgora{
    constructor(){
        this.target = {};
    }

    newTarget(target){
        this.target[target] = {list : [], masterList : []};
    }

    isExist(target){
        if(target in this.target){
            return true;
        }else{
            return false;
        }
    }
    
    push(target, user, msgList){
        try{
            if(!this.isExist(target)){
                this.newTarget(target);
            }
            let memo = "";
            for(let i = 1; i < msgList.length; i++){
                memo += `${msgList[i]} `;
            }
            this.target[target].list.push({user, memo});
            this.target[target].masterList.push({user, memo});
            return `${this.target[target].list.length}번째로 입력되었습니다.`;
        }catch(error){
            console.log(error);
            return "에러가 발생했습니다.";
        }
    }
    insert(target, user, index, msgList){
        try {
            if(!this.isExist(target)){
                this.newTarget(target);
            }
            let memo = "";
            for(let i = 2; i < msgList.length; i++){
                memo += `${msgList[i]} `;
            }
            this.target[target].list.splice(index - 1, 0, {user, memo});
            this.target[target].masterList.splice(index - 1, 0, {user, memo});        
            return `${index}번째로 입력되었습니다.`
        } catch (error) {
            return "에러가 발생했습니다.";
        }
    }
    indexOf(target, userId){
        try{
            if(this.isExist(target)){
                for(let i = 0; i < this.target[target].list.length; i++){
                    if(this.target[target].list[i].user.userId === userId){
                        return i + 1;
                    }
                }
            }
        }catch(error){

        }
        return -1;
    }
    getListString(target) {
        try{
            if(this.isExist(target)){
                let str = "";
                for(let i = 0; i < this.target[target].list.length; i++){
                    str += `${i + 1}. ${this.target[target].list[i].user.displayName}`
                    if(this.target[target].list[i].memo !== ""){
                        str += `/${this.target[target].list[i].memo} `;
                    }else{
                        str += ' ';
                    }
                }
                return str;
            }else{
                return "막고라 리스트가 없습니다.";
            }
        } catch (error) {
            return "에러가 발생했습니다.";
        }
    }
    getMasterListString(target){
        try{
            if(this.isExist(target)){
                let str = "";
                for(let i = 0; i < this.target[target].masterList.length; i++){
                    str += `${i + 1}. ${this.target[target].masterList[i].user.displayName}`
                    if(this.target[target].masterList[i].memo !== ""){
                        str += `/${this.target[target].masterList[i].memo} `;
                    }else{
                        str += ' ';
                    }
                }
                return str;
            }
        } catch (error) {
            return "에러가 발생했습니다.";
        }
    }
    delete(target, index){
        try{
            if(this.isExist(target)){
                if(index === undefined){
                    index = 0;
                    this.target[target].list.splice(index++, 1);
                }else if(isNaN(index)){
                    return "리스트 순번을 입력해주세요.";
                }else if(index >= 1 && index <= this.target[target].list.length){
                    this.target[target].list.splice(index - 1, 1);
                }else{
                    return "에러가 발생했습니다.";
                }
                return `${index}번째 리스트가 삭제되었습니다.`
            }
        } catch (error) {
            return "에러가 발생했습니다.";
        }
    }
    deleteMe(target, userId){
        try{
            if(this.isExist(target)){
                for(let i = 0; i < this.target[target].list.length; i++){
                    if(this.target[target].list[i].user.userId === userId){
                        this.target[target].list.splice(i, 1);
                        return `${i + 1}번째 리스트가 삭제되었습니다.`;
                    }
                }
            }
        } catch (error) {

        }
        return "에러가 발생했습니다.";
    }
}

exports.User = User;
exports.Makgora = Makgora;