import { StyleSheet } from "react-native"

export default StyleSheet.create({
    container:{
        flex: 1,
        marginTop: 50
    }, subject:{
        fontSize: 25,
        fontWeight: 'bold',
        color: 'blue',
    }, row: {
        flexDirection: 'row',
    }, wrap:{
        flexWrap: 'wrap'
    }, margin: {
        margin: 5
    }, avatar: {
        width: 100,
        height: 100,
        borderRadius: 20
    }
})