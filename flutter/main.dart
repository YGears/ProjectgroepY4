import 'dart:async';
import 'dart:convert';

import 'second.dart';
import 'secondScreen.dart';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

Future<Album> fetchAlbum(title) async {
  final response = await http
      .post(Uri.parse('https://iabamun.nl/game/lab-andre/api/index.php/login'),
      body: jsonEncode(<String, String>{
        "name":"Lelouch557",
        "password": "KoekjesZijnGemaaktVanDeeg"
      }),
    );

  print(response.statusCode.toString());
  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return Album.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load album');
  }
}

class Album {
  final String title;

  Album({
    required this.title,
  });

  factory Album.fromJson(Map<String, dynamic> json) {
    return Album(
      title: json['response'],
    );
  }
}

void main() => runApp(const MyApp());

class MyApp extends StatefulWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  var futureAlbum;

  // @override
  // void initState() {
  //   super.initState();
  //   futureAlbum = fetchAlbum("");
  // }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Fetch Data Example',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Builder(
        builder: (context) =>Scaffold(
          appBar: AppBar(
            title: const Text('Fetch Data Example'),
          ),
          body: 
          Center(
            child: buildColumn(context)
          ),
        ),
      )
    );
  }
  Column buildColumn(BuildContext context){
    return Column(
      children:<Widget>[
        TextButton(
          onPressed: (){
            setState(() {
              futureAlbum = fetchAlbum("");
            });
            login(context);
          },
          style: TextButton.styleFrom(padding:EdgeInsets.all(5), backgroundColor: Colors.blue),
          child: Text("Login"),
        )
      ]
    );
  }
  login(BuildContext context){
    Navigator.push(context, 
    MaterialPageRoute(builder: (context) => const MyHomePage(title: 'wat')));
  }
}
