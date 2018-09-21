export default class LoadlevelerJobUtil{
    static findPropById(job, id){
        const { props } = job;
        let prop = null;
        props.forEach(function(a_prop, index){
            if(a_prop.id === id) {
                prop = a_prop
            }
        });
        return prop;
    }

    static getPropTextById(job, id){
        let text = null;
        let prop = LoadlevelerJobUtil.findPropById(job,id);
        if(prop) text = prop.text;
        return text;
    }

    static getPropDataById(job, id){
        let text = null;
        let prop = LoadlevelerJobUtil.findPropById(job,id);
        if(prop) text = prop.data;
        return text;
    }

    static compareString(a,b){
        if(a<b)
            return -1;
        else if(a>b)
            return 1;
        else
            return 0;

    }

    static compareJobStatus(a, b){
        return LoadlevelerJobUtil.compareString(
            LoadlevelerJobUtil.getPropTextById(a, "llq.status"),
            LoadlevelerJobUtil.getPropTextById(b, "llq.status")
        );
    }

    static compareOwner(a, b){
        return LoadlevelerJobUtil.compareString(
            LoadlevelerJobUtil.getPropTextById(a, "llq.owner"),
            LoadlevelerJobUtil.getPropTextById(b, "llq.owner")
        );
    }

    static compareQueueDate(a, b){
        return LoadlevelerJobUtil.compareString(
            LoadlevelerJobUtil.getPropTextById(a, "llq.queue_date"),
            LoadlevelerJobUtil.getPropTextById(b, "llq.queue_date")
        );
    }

    static compareJobClass(a, b){
        return LoadlevelerJobUtil.compareString(
            LoadlevelerJobUtil.getPropTextById(a, "llq.class"),
            LoadlevelerJobUtil.getPropTextById(b, "llq.class")
        );
    }

    static sortJobs(jobs, sort_label, is_asc_order){
        let local_jobs = jobs;
        switch(sort_label){
            case "llq.owner":
                if(is_asc_order)
                    local_jobs.sort(LoadlevelerJobUtil.compareOwner);
                else
                    local_jobs.sort((a,b)=>(-1)*LoadlevelerJobUtil.compareOwner(a,b));
                break;
            case "llq.queue_date":
                if(is_asc_order)
                    local_jobs.sort(LoadlevelerJobUtil.compareQueueDate);
                else
                    local_jobs.sort((a,b)=>(-1)*LoadlevelerJobUtil.compareQueueDate(a,b));
                break;
            case "llq.status":
                if(is_asc_order)
                    local_jobs.sort(LoadlevelerJobUtil.compareJobStatus);
                else
                    local_jobs.sort((a,b)=>(-1)*LoadlevelerJobUtil.compareJobStatus(a,b));
                break;
            case "llq.class":
                if(is_asc_order)
                    local_jobs.sort(LoadlevelerJobUtil.compareJobClass);
                else
                    local_jobs.sort((a,b)=>(-1)*LoadlevelerJobUtil.compareJobClass(a,b));
                break;
            default:
                break;
        }
        return local_jobs;
    }
}