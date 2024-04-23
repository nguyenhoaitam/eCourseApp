import React from "react"
import { View, Text, ActivityIndicator, ScrollView, Image } from "react-native"
import APIS, { endpoints } from "../../configs/APIS"
import MyStyles from "../../Styles/MyStyles"
import { Chip, List, Searchbar } from 'react-native-paper'

const Course = () => {
    const [categories, setCategories] = React.useState(null);
    const[courses, setCourses] = React.useState([]);
    const[loading, setLoading] = React.useState(false);
    const [q, setQ] = React.useState("")


    const loadCates = async () => {
        try {
            let res = await APIS.get(endpoints['categories'])
            setCategories(res.data)
        } catch(ex) {
            console.log(console.error(ex))
        }
    }

    const loadCourse = async () => {
        try {
            let url = `${endpoints['courses']}?q=${q}`
            let res = await APIS.get(url)
            setCourses(res.data.results)
        } catch(ex) {
            console.log(console.error(ex))
        } finally {
            setLoading(false)
        }
    }

    React.useEffect(() => {
        loadCates();
    }, []);

    React.useEffect(() => {
        loadCourse();
    }, [q]);

    return (
        <View style={[MyStyles.container]}>
            <View style={[MyStyles.row, MyStyles.wrap]}>
                {categories===null?<ActivityIndicator/>:<>
                    {categories.map(c => <Chip style={MyStyles.margin} key={c.id} icon="shape">{c.name}</Chip>)}
                </>}
            </View>
            <View>
            <Searchbar
                placeholder="Nhap tu khoa..."
                onChangeText={setQ}
                value={q}
            />
            </View>
            <ScrollView style={MyStyles.margin}>
                {courses.map(c => <List.Item key={c.id} title={c.subject} description={c.created_date} left={() => <Image style={MyStyles.avatar} source={{uri: c.image}}/>}/>)}
                {loading && <ActivityIndicator/>}
            </ScrollView>
        </View>
    )
}


export default Course